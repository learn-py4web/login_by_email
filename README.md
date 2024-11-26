# Login by email

This app provides a very simple example of how to implement login by email. 
The logic is in `auth_by_email.py`.  Basically, in `common.py` there is a line: 

```python
auth = AuthByEmail(session)
```

One can then check whether the user is logged in via: 

```python
@action.uses('mypage.html', auth)
```

and one can enforce login via: 

```python
@action.uses('mypage.html', auth.enforce)
```

One can get the email of the user via: 

```python
email = auth.get_email()
```

The implementation uses only the session; no additional auth tables are needed. 


