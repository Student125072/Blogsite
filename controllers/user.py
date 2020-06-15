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


def edit():
    current_username = auth.user.username
    return dict(edit=auth.profile(next=URL('user', 'profile', vars={
        'username': current_username
    })))
