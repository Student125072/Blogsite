db.define_table('rant',
                Field('author', 'reference auth_user', writable=False, default=auth.user_id),
                Field('title', length=50, requires=IS_NOT_EMPTY()),
                Field('description', 'text', length=500, requires=IS_NOT_EMPTY()),
                Field('posted_at', 'datetime', requires=IS_NOT_EMPTY(), writable=False),
                Field('tag', requires=IS_IN_SET([
                    'Front-end', 'Back-end'
                ]))
                )

db.define_table('reply',
                Field('author', 'reference auth_user', writable=False, default=auth.user_id),
                Field('rant_id', 'reference rant', writable=False),
                Field('description', 'text', length=500, requires=IS_NOT_EMPTY()),
                Field('posted_at', 'datetime', requires=IS_NOT_EMPTY(), writable=False)
                )
