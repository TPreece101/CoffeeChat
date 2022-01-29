import random
import itertools

def chunk_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]


def divide_users(users, group_size):
    if len(users) < group_size:
        return [users]

    # Will make sure each group has at least group_size members
    num_leftover = len(users) % group_size
    leftover_users = random.sample(users, num_leftover)

    for user in leftover_users:
        users.remove(user)
    
    random.shuffle(users)

    groups = list(chunk_list(users, group_size))

    for group in itertools.cycle(groups):
        if len(leftover_users) > 0:
            user = leftover_users.pop(0)
            group.append(user)
        else:
            break
    
    return groups



# users = [
#     "Mark", "Amber", "Todd", "Anita", "Sandy", "Bob", "Fred", "Abdul", "Barry", "Sarah", "Eleana", "Lee", "Jamie"
# ]
# users =['Tom']

# t = divide_users(users, 4)