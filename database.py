from sqlalchemy import create_engine, text


engine = create_engine("mysql+mysqldb://fsry1f078196ijjoxgqw:pscale_pw_tHrAC62oq9SEyGFVp2bQ8jb8Ik9mYO84bwgcogwNAJG@aws.connect.psdb.cloud/mindnex",
                            pool_recycle=3600, echo=True)

