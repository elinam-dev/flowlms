#!/usr/bin/env python3
"""
Rename hr_analytics images according to correct order mapping.
Format: current_num -> correct_position
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')
client = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = client[os.environ['DB_NAME']]

BASE_URL = "https://flowlms-production.up.railway.app"
IMG_DIR = ROOT_DIR / "uploads" / "images" / "HR" / "hr_analytics"

# Mapping: current number -> correct slide position
# Based on user's specification:
# 1->1, 27->2, 28->3, 2->4, 3->5, 29->6, 30->7, 4->8, 5->9, 6->10, 7->11,
# 31->12, 32->13, 8->14, 33->15, 9->16, 10->17, 34->18, 11->19, 35->20, 36->21,
# 12->22, 13->23
# Then continuing the pattern: 37->24, 38->25, 14->26, 39->27, 40->28, 41->29,
# 42->30, 43->31, 44->32, 45->33, 46->34, 15->35, 16->36, 47->37, 48->38,
# 49->39, 50->40, 51->41, 52->42, 53->43, 17->44, 18->45, 54->46, 55->47,
# 56->48, 57->49, 58->50, 19->51, 20->52, 59->53, 60->54, 61->55, 62->56,
# 63->57, 64->58, 65->59, 66->60, 21->61, 67->62, 68->63, 69->64, 70->65,
# 71->66, 72->67, 73->68, 22->69, 74->70, 75->71, 76->72, 77->73, 78->74,
# 79->75, 80->76, 23->77, 81->78, 82->79, 83->80, 84->81, 85->82, 86->83,
# 87->84, 24->85, 25->86, 88->87, 89->88, 90->89, 91->90, 26->91, 92->92,
# 93->93, 94->94, 95->95, 96->96, 97->97, 98->98, 99->99, 101->100, 100->101,
# 102->102, 103->103, 104->104, 105->105, 106->106, 107->107, 108->108,
# 109->109, 110->110, 111->111, 112->112, 113->113, 114->114, 115->115,
# 116->116, 117->117, 118->118, 119->119, 120->120, 121->121, 122->122,
# 123->123, 124->124, 125->125

MAPPING = [
    1, 27, 28, 2, 3, 29, 30, 4, 5, 6, 7, 31, 32, 8, 33, 9, 10, 34, 11, 35, 36,
    12, 13, 37, 38, 14, 39, 40, 41, 42, 43, 44, 45, 46, 15, 16, 47, 48, 49, 50,
    51, 52, 53, 17, 18, 54, 55, 56, 57, 58, 19, 20, 59, 60, 61, 62, 63, 64, 65,
    66, 21, 67, 68, 69, 70, 71, 72, 73, 22, 74, 75, 76, 77, 78, 79, 80, 23, 81,
    82, 83, 84, 85, 86, 87, 24, 25, 88, 89, 90, 91, 26, 92, 93, 94, 95, 96, 97,
    98, 99, 101, 100, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
    114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125
]

async def fix():
    # Step 1: rename all to temp
    for i in range(1, 126):
        src = IMG_DIR / f"hr_analytics_slide_{i:03d}.jpeg"
        tmp = IMG_DIR / f"tmp_{i:03d}.jpeg"
        if src.exists():
            src.rename(tmp)

    # Step 2: rename from temp to correct position
    for new_pos, old_num in enumerate(MAPPING, 1):
        tmp = IMG_DIR / f"tmp_{old_num:03d}.jpeg"
        dst = IMG_DIR / f"hr_analytics_slide_{new_pos:03d}.jpeg"
        if tmp.exists():
            tmp.rename(dst)
            print(f"  old_{old_num:03d} -> slide_{new_pos:03d}")
        else:
            print(f"  WARNING: tmp_{old_num:03d} not found!")

    # Step 3: rebuild lessons in DB
    course = await db.courses.find_one(
        {'title': {'$regex': 'hr analytics', '$options': 'i'}},
        {'_id': 0, 'id': 1}
    )
    modules = await db.modules.find({'course_id': course['id']}).to_list(None)
    module_ids = [m['id'] for m in modules]
    await db.lessons.delete_many({'module_id': {'$in': module_ids}})

    for i in range(1, 126):
        filename = f"hr_analytics_slide_{i:03d}.jpeg"
        url = f"{BASE_URL}/uploads/images/HR/hr_analytics/{filename}"
        content = f'<div style="text-align: center; padding: 20px;"><img src="{url}" alt="Slide {i}" style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></div>'
        await db.lessons.insert_one({
            "id": str(uuid.uuid4()),
            "module_id": modules[0]["id"],
            "title": f"Slide {i}",
            "content_type": "text",
            "content": content,
            "duration_minutes": 3,
            "order": i - 1
        })

    print(f"\nDone! Rebuilt 125 lessons in correct order.")

if __name__ == "__main__":
    asyncio.run(fix())
