import nltk.tree as tree

# 递归遍历
def test(t):
    if isinstance(t, str):
        print (t)
    else:
        for i in range(len(t)):
            test(t[len(t)-i-1])


# 非递归遍历
def test_2(t):
    stack = []
    stack.append(t)

    current = ""
    while stack:
        current = stack.pop()

        if isinstance(current, tree.Tree):
            for i in range(len(current)):
                stack.append(current[i])

        elif isinstance(current, str):
            # print "[输出] ",current
            print (current)


if __name__ == "__main__":
    C = tree.Tree("我", ["E", "F"])
    B = tree.Tree("是", [C, "D"])
    H = tree.Tree("好", ["M", "N"])
    A = tree.Tree("人", ["G", H])
    root = tree.Tree("Root", [A, B])


    print (root[0])
    print (root.height())
    print( len(root))
    print (type(root))

    test(root)
    # test_2(root)

    root.draw()
# --------------------- 
# 作者：南宫木java 
# 来源：CSDN 
# 原文：https://blog.csdn.net/u012022003/article/details/53815901 
# 版权声明：本文为博主原创文章，转载请附上博文链接！