from benchmark import session_scope, PersonDeclarative, AddressDeclarative


# add 'npeople' people to the database and then query them
def bench_sqlalchemy_combined(loops=3, writes=7, reads=70):
    for loops in range(loops):
        with session_scope() as session:
            if writes > 0:
                # drop rows created by the previous benchmark
                session.query(PersonDeclarative).delete(synchronize_session=False)
                session.query(AddressDeclarative).delete(synchronize_session=False)
                for i in range(writes):
                    # Insert a Person in the person table
                    new_person = PersonDeclarative(name="name %i" % i)
                    session.add(new_person)
                    session.commit()

                    # Insert an Address in the address table
                    new_address = AddressDeclarative(post_code='%05i' % i, person=new_person)
                    session.add(new_address)
                    session.commit()

            if reads > 0:
                for _ in range(reads):
                    session.query(PersonDeclarative).all()
