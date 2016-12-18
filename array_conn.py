def resolve(arr, args, limit=30):
    # alen = len(arr)
    first = args.get('first')
    last = args.get('last')
    before = args.get('before')
    after = args.get('after')

    # limits
    if first > limit:
        first = limit

    if last > limit:
        last = limit

    if first and after:
        return arr[after:after+first]
    if first:
        return arr[:first]
    if after:
        return arr[after:after+limit]
    if last and before:
        return arr[before-last:before]
    if last:
        return arr[-last:]
    if before:
        return arr[before-limit:before]
    return arr[:limit]
