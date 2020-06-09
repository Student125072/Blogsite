import datetime


@auth.requires_login()
def create():
    form = SQLFORM.factory(db.rant)

    if form.process().accepted:
        session.flash = 'Well done, you ranted!'
        rant_id = db.rant.insert(
            author=auth.user_id,
            title=form.vars.title,
            description=form.vars.description,
            posted_at=datetime.datetime.now(),
            tag=form.vars.tag
        )
        redirect(URL(f='view', vars={'id': rant_id}))

    return dict(form=form)


def view():
    if request.vars['id']:
        rant_id = request.vars['id']

        if auth.user:
            reply_form = SQLFORM.factory(db.reply)
            if reply_form.process().accepted:
                db.reply.insert(
                    author=auth.user_id,
                    rant_id=rant_id,
                    description=reply_form.vars.description,
                    posted_at=datetime.datetime.now()
                )
                session.flash = 'Comment added!'
                redirect(URL(f='view', vars={'id': rant_id}))

        this_rant = db(db.rant.id == rant_id).select().first()
        rant_comments = db(db.reply.rant_id == rant_id).select()
        return dict(rant=this_rant, comments=[comment for comment in rant_comments if rant_comments], reply_form=reply_form)
    else:
        raise HTTP(404)
