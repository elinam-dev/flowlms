import os

folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\Finance\financial_statements"
screenshots = sorted([f for f in os.listdir(folder) if f.startswith('Screenshot')])
for i, f in enumerate(screenshots, start=1):
    src = os.path.join(folder, f)
    dst = os.path.join(folder, f'financial_statements{i}.jpeg')
    os.rename(src, dst)
    print(f'{f} -> financial_statements{i}.jpeg')
print(f'Done: {len(screenshots)} files renamed')
