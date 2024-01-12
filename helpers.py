from http.cookies import SimpleCookie
import json

def create_books_html(list_of_books_dict):
    html = ""
    for book in list_of_books_dict:
        html += "<tr>"
        html += f"<td>{book['isdn']}</td>"
        html += f"<td>{book['title']}</td>"
        html += f"<td>{book['author']}</td>"
        html += f"<td>{book['quantity']}</td>"
        html += f"<td>{book['status']}</td>"
        html += f"<td>{book['genre']}</td>"
        html += "</tr>"
    return html
def create_users_html(list_of_users_dict):
    html = ""
    for user in list_of_users_dict:
        html += "<tr>"
        html += f"<td>{user['firstname']}</td>"
        html += f"<td>{user['lastname']}</td>"
        html += f"<td>{user['email']}</td>"
        html += f"<td>{user['current_borrow']}</td>"
        html += "</tr>"
    return html
def create_transactions_html(list_of_transactions_dict):
    html = ""
    for transaction in list_of_transactions_dict:
        html += "<tr>"
        html += f"<td>{transaction['id']}</td>"
        html += f"<td>{transaction['username']}</td>"
        html += f"<td>{transaction['bookid']}"
        html += f"<td>{transaction['datetime']}</td>"
        html += f"<td>{transaction['action']}</td>"
        html += "</tr>"
    return html
def is_session_authenticated(headers):
    """Return Email if session is assigned to the email 
    user session_auth.txt to store sessionids 
    """
    cookies = SimpleCookie(headers.get('Cookie'))
    if cookies.get('sessionid') == None:
        return False
    sessionid = cookies['sessionid'].value
    with open('session_auth.txt','r') as session_auth_file:
        auth_sessions = session_auth_file.read()
        auth_sessions = json.loads(auth_sessions)
    for email in auth_sessions.keys():
        if sessionid in auth_sessions[email]:
            return  email
    return False

def remove_session(headers):
        cookies = SimpleCookie(headers.get('Cookie'))
        if cookies.get('sessionid'):
            session_id = cookies['sessionid'].value
            with open('session_auth.txt','r') as file:
                auth_sessions = file.read()
                auth_sessions = json.loads(auth_sessions)
                for email in auth_sessions:
                    for present_id in auth_sessions[email]:
                        if present_id == session_id:
                            auth_sessions[email].remove(session_id)
            with open('session_auth.txt','w') as file:
                file.write(json.dumps(auth_sessions))   

def add_session(email,sessionid):
        with open('session_auth.txt','r') as session_auth_file:
            auth_sessions = session_auth_file.read()
            auth_sessions = json.loads(auth_sessions)
        if email in auth_sessions:
            auth_sessions[email].append(sessionid)
        else: auth_sessions[email] = [sessionid]
        with open('session_auth.txt','w') as session_auth_file:
            session_auth_file.write(json.dumps(auth_sessions))