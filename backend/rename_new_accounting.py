import os

folder = r"c:\Users\User\Desktop\flowlms\flowlms\backend\uploads\images\Finance\the_accounting_cycle"
screenshots = sorted([f for f in os.listdir(folder) if f.startswith('Screenshot')])
for i, f in enumerate(screenshots, start=70):
    src = os.path.join(folder, f)
    dst = os.path.join(folder, f'the_accounting_cycle{i}.jpeg')
    os.rename(src, dst)
    print(f'{f} -> the_accounting_cycle{i}.jpeg')
print(f'Done: {len(screenshots)} files renamed')
