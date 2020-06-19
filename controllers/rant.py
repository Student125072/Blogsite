import datetime
from web2py_utils.paginate import Pagination


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


@auth.requires_login()
def delete():
    if not request.vars:
        return '??'
    rant_id = request.vars['rant_id']
    rant = db.rant[rant_id]
    if not rant:
        raise NotImplementedError('Rant not found.')
    if rant.author != auth.user_id:
        session.flash = 'You do not have permission to do this.'
        redirect(URL(f='feed'))
    try:
        db(db.rant.id == rant_id).delete()
        db.commit()
        session.flash = 'Rant has been deleted succesfully.'
        redirect(URL(f='manage'))
    except Exception:
        raise


@auth.requires_login()
def manage():
    query = db.rant.author == auth.user_id
    orderby = ~db.rant.posted_at
    pcache = (cache.ram, 15)
    paginate = Pagination(db, query, orderby, display_count=10, cache=pcache, r=request, res=response)

    rants = paginate.get_set(set_links=True)

    return dict(rants=rants)


def view():
    if request.vars['id']:
        rant_id = request.vars['id']
        this_rant = db(db.rant.id == rant_id).select().first()
        rant_comments = db(db.reply.rant_id == rant_id).select()

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
            return dict(rant=this_rant, comments=[comment for comment in rant_comments if rant_comments],
                        reply=reply_form)

        return dict(rant=this_rant, comments=[comment for comment in rant_comments if rant_comments])
    else:
        raise HTTP(404)


def feed():
    query = db.rant.id > 0
    orderby = ~db.rant.posted_at
    pcache = (cache.ram, 15)
    if request.vars['tag']:
        if request.vars['tag'] == 'Front-end':
            query = db.rant.tag == 'Front-end'
        elif request.vars['tag'] == 'Back-end':
            query = db.rant.tag == 'Back-end'
        else:
            raise HTTP(404)

    paginate = Pagination(db, query, orderby, display_count=10, cache=pcache, r=request, res=response)

    rants = paginate.get_set(set_links=True)

    return dict(rants=rants)
