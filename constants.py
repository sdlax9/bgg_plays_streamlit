DATE_BINS = [
    30,
    365,
    None,
]

DATE_BIN_TABS = []
for date_bin in DATE_BINS:
    if date_bin:
        DATE_BIN_TABS.append(f'Last {date_bin} Days')
    else:
        DATE_BIN_TABS.append('All Time')