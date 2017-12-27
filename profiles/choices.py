PEOPLE = (
    ('', ('All people')),
    ('me/non-friends/', ('Non-friends')),
    ('me/friends/', ('Friends')),
    ('me/friends/friends/', ('Friends of friends')),
)

GENDER = (
    ('', ('All')),
    ('females/', ('Female')),
    ('males/', ('Male')),
)

INTERESTED_IN = (
    ('', ('All')),
    ('females/users-interested/', ('Women')),
    ('males/users-interested/', ('Men')),
)

RELATIONSHIP = (
    ('', ('All')),
    ('single/users/', ('Single')),
    ('in-any-relationship/users/', ('In a Relationship')),
    ('in-open-relationship/users/', ('In an Open Relationship')),
    ('married/users/', ('Married')),
    ('in-civil-union/users/', ('In a Civil Union')),
    ('in-domestic-partnership/users/', ('In a Domestic Partnership')),
    ('engaged/users/', ('Engaged')),
    ('its-complicated/users/', ("It's Complicated")),
    ('widowed/users/', ('Widowed')),
    ('separated/users/', ('Separated')),
    ('divorced/users/', ('Divorced')),
    ('dating/users/', ('Dating')),
)


LOCATION = (
    ('{}/residents/present/', ('Current location')),
    ('{}/residents/past/', ('Former location')),
    ('{}/visitors/', ('Visited')),
    ('{}/home-residents/', ('From')),
    ('{}/residents-near/present/', ('Lives near')),
)

COMPANY = (
    ('{}/employees/present/', ('Current')),
    ('{}/employees/past/', ('Former')),
)

SCHOOL = (
    ('{}/students/present/', ('Current')),
    ('{}/students/past/', ('Former')),
)

MONTHS = (
    ('', ('Month')),
    ('jan', ('Jan')),
    ('feb', ('Feb')),
    ('mar', ('Mar')),
    ('apr', ('Apr')),
    ('may', ('May')),
    ('jun', ('Jun')),
    ('jul', ('July')),
    ('aug', ('Aug')),
    ('sep', ('Sep')),
    ('oct', ('Oct')),
    ('nov', ('Nov')),
    ('dec', ('Dic')),
)

BORN = (
    ('date', ('Born')),
    ('range', ('Born (range)')),
)
