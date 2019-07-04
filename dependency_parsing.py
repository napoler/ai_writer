# import os
# os.chdir("../")   #修改当前工作目录
# print(os.getcwd())    #获取当前工作目录
import libs



# print('svos', svos)

# def get_next(item,arcs):
#     if item[2]< item[5]:


def get_child(item,arcs):
    """    
    # next_id 代表id较大的
    # pre_id 代表id较小的
    """
 
        
    next_item =[]
    pre_item =[]
    if item[2] > item[5]:
        next_id  = item[2]
        pre_id  = item[5]
    else:
        next_id  = item[5]
        pre_id  = item[2]
    # next_id
    # pre_id
    for it in arcs:
        if it ==item:
            #数据相同代表本数据
            continue
        if it[2] ==next_id or it[5] ==next_id:
            #向后推进数据
            if it[2] > next_id or it[5] > next_id:
                next_item.append(it)
            else:
                pre_item.append(it)

        # if it[2] ==pre_id or it[5] ==pre_id:
        #     #往前发展
        #     pass

        # if it[5] ==pre_id:
            
        #     #往前发展
        #     if it[2] < it[5]:
        #         pre_item.append(it)
        #     else:
        #         pre_item.append(it)

        # if it[5] ==item[5] and it[2]>it[5]:
        #     nexti.append(it)
    # if len(next_item)==0:
    #     i=[]
    
    # child.append(next_item)
        # print('##'*10)
    child = {'middle':item,'pre_item':pre_item,'next_item':next_item}
    # print('\n',child,'\n\n')
    return child
 


# def auto_choice_child(item,arcs):
#     child = get_child(item,arcs)
#     for item in next_item:
#         child = get_child(item,arcs)
#         if len(child['next_item'])>0:
#             auto_choice_child(child['next_item'],arcs)
#         else:
#             # recurve_opt(target_file)
#             pass

def get_big_next(item):

    if item[2] > item[5]:
        next_id  = item[2]
        pre_id  = item[5]
    else:
        next_id  = item[5]
        pre_id  = item[2]
    return pre_id,next_id

def choice_child(item,arcs,way):
    end = 0
    print(item)
    print(way)
    pre_id,next_id = get_big_next(item)
    # print(pre_id)
    # print(next_id)

    if len(way)==0:
        way.append(pre_id)
    way.append(next_id)
    
    child = get_child(item,arcs)
    if len(child['next_item'])>0:
        for it in child['next_item']:

            # pre_id,next_id = get_big_next(it)
            
            m_way,end = choice_child(it,arcs,way)
            # way.append(next_id)
            # if end==1:
                


    else:
        # way
        # w_path.append(way)
        # print(item)
        # way =[]
        # w_path.append(way)
        print("结束!")
        end = 1
        pass
    # choice_child(item,arcs,way,w_path)
    return way,end


    

    # pass

def run():
    # import fun
    extractor =libs.TripleExtractor()
    content1 = """它们的胆子很大也相当机警能高度警惕地守护家园是最受欢迎的小型护卫犬之一"""

    # svos,Branchs,my = extractor.triples_main(content1)
    # print('svos', svos)
    # print('Branchs',Branchs)
    # print('my',my)

    # print('content1', content1)

    svos= extractor.triples_try(content1)
    for words, postags, child_dict_list, roles_dict, arcs  in svos:
        print('#'*100)
        # choice_child(arcs)
        # for item in arcs:
        #     get_child(item,arcs)
        t  =arcs[2]
        way=[]
        w_path=[]
        choice_child(t,arcs,way)



run()















# def get_child(arcs):
#     tree = []
#     for item in arcs:
        
#         i =[]
#         nexti =[]
#         for it in arcs:
            
#             if it[2] ==item[5]:
#                 i.append(it)
#             if it[5] ==item[5] and it[2]>it[5]:
#                 nexti.append(it)
#         if len(i)==0:
#             i=[]
        
#         tree.append({'r':item,'child':i,'nexti':nexti})
#         # print('##'*10)

#         # print((item,i))
#     return tree

# def get_next(item):


# def choice_child_auto( path_list,new_tree):
#     """自动预测下一个字符是否是可以继续的"""
#     last = path_list[-1]
#     # print('path_list',path_list)
#     # print('last',last)
#     # pre = last[0]
#     # next= last[1]
#     pre = new_tree[last]['r'][2]
#     next = new_tree[last]['r'][5]
#     print('pre',pre)
#     print('next',next)

#     next_ids =[]
#     tree = []
#     if pre > next:
#         print("前一个大于后一个不服 ")
#         pass
#     else:
#         print("继续预测")
#         print(new_tree[next])
#         get_next(new_tree[next])
#         # for item in new_tree[next]['child']:
#         #     print('item newx',item)
#         #     print('path_list',path_list)
#         #     if item[2]> next:
#         #         next_ids.append(item[2])
#         #         new = path_list
#         #         new.append(item[5])
#         #         new.append(item[2])

#         #         print(new)
#         pass


#     # for next in  next_ids:
#     # while len(next_ids)>0:

#     #     for next in next_ids:
#     #         next_ids,slist = choice_child_auto(pre,next,new_tree)
#     # print('next_ids',next_ids)

#     return next_ids


# # def list_add(list1,list2):
# #     new_list =[]
# #     temp_list=list1
# #     for t in list2:
# #         # temp_list=list1
# #         # print(list1)
# #         # temp_list.append(t)
# #         # print(temp_list)
        
# #         new_list.append(list_add_one(list1,t))
# #         list1 =temp_list
# #     return new_list
        
# # def list_add_one(list1,one):

# #     list1.append(one)
# #     print(list1)
# #     return list1



# def choice_child(arcs):
#     # item['r'][2]
#     new_tree = get_child(arcs)
#     print(new_tree)
#     c_ids=[]
#     # pre_id=0
#     ls = []
#     for item in new_tree:
#         # print('222*****')
#         l = []
#         #如果是顺序则执行预测
#         if item['r'][2] < item['r'][5]:


#             l_mini=[item['r'][2],item['r'][5]]
#         #     old_l_mini = l_mini
#             next_ids = choice_child_auto(l_mini,new_tree)
#             print(next_ids)
#             # for 
        
#         #     while len(next_ids)>0:
#         #         # l_mini=[item['r'][2],item['r'][5]]
                
#         #         #  print(next_ids)
#         #         for n_id in  next_ids:
#         #             next_ids = choice_child_auto(l_mini,new_tree)
#         #             l_mini.append(n_id)
#         #         l.append(l_mini)

#         #         l_mini = old_l_mini
#         # if len(l)>0: 
#         #     ls.append(l)
#     print(ls)


#         # if len(item['child'])>1 and item['r'][2] > pre_id :
#         #     # print('继续')

#         #     for it in item['child']:

#         #         if it[2]>item['r'][2]:
#         #             print('可以继续')
#         #             c_ids.append(it[2])
                
#     #     # print(c_ids)
        
#     #     # for id in c_ids:
#     #     #     choice_child(new_tree[id])
#     # return c_ids




# tree =[]
# for words, postags, child_dict_list, roles_dict, arcs  in svos:
#     print('1000000000###'*100)
#     choice_child(arcs)
#     # list1 =['q','e','r']
#     # list2 =['q1','e1','r1']
#     # a = list_add(list1,list2)
#     # print(a)



#     # print(arcs)
#     # new_tree = get_child(arcs)
#     # print('new_tree',new_tree)
#     # path_list= [new_tree[0]['r'][2],new_tree[0]['r'][5]]
#     # # for item in new_tree:
#     # next_ids= choice_child_auto(path_list,new_tree)
#     # # print(next_ids)
#     # # pre,next_ids = choice_child_auto(0,2,new_tree)
#     # print(next_ids)

#     # next =  []
#     # while len(next)>0:
#     #     pre,next_ids = choice_child_auto(pre,next,new_tree):

# # print(new_tree)

# # i = 1
# # # print(len(new_tree))
# # pre_id = 0
# # m_tree = []
# # c_tree =[]
# # for item in new_tree:
# #     # print(item['r'][2])
# #     if len(item['child'])>1 and item['r'][2] > pre_id :
# #         m_tree.append(item['r'][1])
# #         # print(item['child'])
# #         c_ids = choice_child(item)




# #     if len(item['child'])>1 and item['r'][2] > pre_id or i==1 or len(new_tree)==i:
# #         m_tree.append(item['r'][1])



# #         # print('子元素:',len(item['child']))
# #     # if i==1:
# #     #     # print('第一个')
# #     #     print(item['r'][1])
# #     #     # print(len(item['child']))
# #     # if len(new_tree)==i:
# #     #     # print('最后一个')
# #     #     print(item['r'][1])
# #     #     # print(len(item['child']))
# #     else:
# #         c_tree.append(item['r'][1])
# #     pre_id = item['r'][2]
# #     i = i +1 
# # print('m_tree',m_tree)
# # print('c_tree',c_tree)
