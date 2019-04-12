from micro import session_scope, session_scope2, Person, Person2, Address, Address2


# add 'npeople' people to the database and then query them
def bench_sqlalchemy(loops=3, writes=7, reads=70):
    for loops in range(loops):
        with session_scope() as session:
            if writes > 0:
                # drop rows created by the previous micro
                session.query(Person).delete(synchronize_session=False)
                session.query(Address).delete(synchronize_session=False)
                for i in range(writes):
                    # Insert a Person in the person table
                    new_person = Person(name="name %i" % i)
                    session.add(new_person)
                    session.commit()

                    # Insert an Address in the address table
                    new_address = Address(post_code='%05i' % i, person=new_person)
                    session.add(new_address)
                    session.commit()

            if reads > 0:
                for _ in range(reads):
                    session.query(Person).all()


# add 'npeople' people to the database and then query them
def bench_sqlalchemy2(loops=10, writes=10, reads=100):
    for loops in range(loops):
        with session_scope2() as session2:
            if writes > 0:
                # drop rows created by the previous micro
                session2.query(Person2).delete(synchronize_session=False)
                session2.query(Address2).delete(synchronize_session=False)
                for i in range(writes):
                    # Insert a Person in the person table
                    new_person = Person2(name="name %i" % i)
                    session2.add(new_person)
                    session2.commit()

                    # Insert an Address in the address table
                    new_address = Address2(post_code='%05i' % i, person=new_person)
                    session2.add(new_address)
                    session2.commit()

            if reads > 0:
                for _ in range(reads):
                    session2.query(Person2).all()
