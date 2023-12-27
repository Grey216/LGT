from cqueue import CDQueue,CLLQueue,QFullError


if __name__ == "__main__":
    q = CLLQueue[str](10)
    for i in range(10):
        q.push(str(i))
    print(q)
    q.resize(7)
    print(q)
    try:
        q.push("asd")
    except QFullError as er:
        print(er)
        q.push("asd",replace=True)
    print(q)
    print(q.pop())
    q.insert(3,"zxc")
    print(q)
    print(q.front())
    print(q.back())