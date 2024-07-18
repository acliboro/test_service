import os
import redis

def get_redis_inst():
    #username
    #password will include later
    # user_connection = redis.Redis(host='0.0.0.0', port=6379, decode_responses=True)
    user_connection = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    return user_connection

def main():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    # r = get_redis_inst()
    r.set('foo', 'bar')
    print(r.get('foo'))
    print(r.keys())
    print(r.get('all_posts'))
    print(r.delete('all_posts'))
    print(r.keys())

if __name__ == "__main__":
    main()



    