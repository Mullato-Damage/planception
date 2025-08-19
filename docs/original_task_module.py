# Messy starter code for "task manager" utilities

from datetime import datetime, timedelta

TASKS = []

def add(n, d, p, c):
    # n=name, d=due (string), p=priority str, c=category
    # due string format "MM-DD-YYYY"
    if n == "" or n is None:
        print("bad name")
        return
    try:
        due = datetime.strptime(d, "%m-%d-%Y")
    except:
        print("bad date")
        return
    if p not in ["low","med","high"]:
        print("bad priority")
        return
    t = {"name": n.strip(), "due": due, "priority": p, "category": c}
    # prevent duplicates by name (case insensitive)
    for i in range(len(TASKS)):
        if TASKS[i]["name"].lower() == t["name"].lower():
            print("dup")
            return
    TASKS.append(t)
    # sort tasks by due date
    TASKS.sort(key=lambda x: x["due"])

def overdue():
    # print overdue ones
    now = datetime.now()
    o = []
    for t in TASKS:
        if t["due"] < now:
            o.append(t)
    for t in o:
        print(t["name"], t["due"].strftime("%m-%d-%Y"), t["priority"], t["category"])
    return o

def today():
    # print today & high priority first
    td = datetime.now().date()
    lst = []
    for t in TASKS:
        if t["due"].date() == td:
            lst.append(t)
    # bubble 'high' first then 'med' then 'low' (ugly)
    hi = []
    me = []
    lo = []
    for t in lst:
        if t["priority"] == "high":
            hi.append(t)
        elif t["priority"] == "med":
            me.append(t)
        else:
            lo.append(t)
    r = hi + me + lo
    for t in r:
        print(t["name"], t["due"].strftime("%m-%d-%Y"), t["priority"])
    return r

def filterCat(cat):
    out = []
    for t in TASKS:
        if t["category"] == cat:
            out.append(t)
    return out

def rm(n):
    # remove by name (assumes unique)
    idx = -1
    for i in range(len(TASKS)):
        if TASKS[i]["name"].lower() == n.lower():
            idx = i
    if idx != -1:
        del TASKS[idx]
    else:
        print("not found")

def demo():
    add("  Essay  ", "08-01-2025", "high", "School")
    add("groceries","08-09-2025","low","Life")
    add("groceries","08-09-2025","low","Life") # dup
    add("", "bad", "nope", "X")
    overdue()
    today()
    print([x["name"] for x in filterCat("Life")])
    rm("Essay")
    rm("Essay")

if __name__ == "__main__":
    demo()