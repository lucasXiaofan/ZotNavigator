def memory_manager(queue,query):
     
    while len(queue) > 10: 
        queue.pop(0)
    queue.append(query)
    return ", ".join(queue)
