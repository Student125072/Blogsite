def profile():
    if request.vars['username']:
        username = request.vars['username']
        this_user = db(db.auth_user.username == username).select().first()
        if this_user:
            posts_count = db(db.rant.author == this_user.id).count()
            posts = db(db.rant.author == this_user.id).select(orderby=~db.rant.posted_at)

            if this_user.id == auth.user_id:

                if request.vars['edit']:
                    return dict(edit_profile=auth.profile(), user=this_user, posts_count=posts_count)
                return dict(user=this_user, posts_count=posts_count, posts=posts)

            return dict(user=this_user, posts_count=posts_count, posts=posts)


def register():
    return dict(register=auth.register())


def login():
    return dict(login=auth.login())