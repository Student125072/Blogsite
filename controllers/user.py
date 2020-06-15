def profile():
    if request.vars['username']:
        username = request.vars['username']
        this_user = db(db.auth_user.username == username).select().first()
        if this_user:
            posts_count = db(db.rant.author == this_user.id).count()
            posts = db(db.rant.author == this_user.id).select(orderby=~db.rant.posted_at)

            return dict(user=this_user, posts_count=posts_count, posts=posts)


def register():
    return dict(register=auth.register())


def login():
    return dict(login=auth.login())


def change_password():
    return dict(change_password=auth.change_password(next=URL('user', 'profile', vars={
        'username': auth.user.username
    })))


def retrieve_password():
    return dict(retrieve_password=auth.retrieve_password())


def edit():
    return dict(edit=auth.profile(next=URL('user', 'profile', vars={
        'username': auth.user.username
    })))
