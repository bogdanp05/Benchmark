from benchmark import session_scope_declarative, PersonDeclarative, AddressDeclarative, Person_imperative, \
    Address_imperative, session_scope_imperative


# add 'npeople' people to the database
def bench_sqlalchemy_declarative(loops, npeople):
    for loops in range(loops):
        with session_scope_declarative() as session:
            # drop rows created by the previous benchmark
            session.query(PersonDeclarative).delete(synchronize_session=False)
            session.query(AddressDeclarative).delete(synchronize_session=False)

            for i in range(npeople):
                # Insert a Person in the person table
                new_person = PersonDeclarative(name="name %i" % i)
                session.add(new_person)
                session.commit()

                # Insert an Address in the address table
                new_address = AddressDeclarative(post_code='%05i' % i, person=new_person)
                session.add(new_address)
                session.commit()

            # do 100 queries per insert
            for i in range(npeople):
                session.query(PersonDeclarative).all()


# add 'npeople' people to the database
def bench_sqlalchemy_imperative(loops, npeople):
    for loops in range(loops):
        # drop rows created by the previous benchmark
        cur = Person_imperative.delete()
        cur.execute()

        cur = Address_imperative.delete()
        cur.execute()

        for i in range(npeople):
            # Insert a Person in the person table
            new_person = Person_imperative.insert()
            result_proxy = new_person.execution_options(autocommit=True).execute(name="name %i" % i)

            # Insert an Address in the address table
            new_address = Address_imperative.insert()
            new_address.execution_options(autocommit=True).\
                execute(post_code='%05i' % i, person_id=result_proxy.inserted_primary_key[0])

        # do 'npeople' queries per insert
        for i in range(npeople):
            cur = Person_imperative.select()
            cur.execute()
