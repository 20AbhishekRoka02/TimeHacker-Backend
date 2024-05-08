
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os
load_dotenv()

# POSTGRES_URL="postgres://default:zQP9da1wetiY@ep-hidden-sun-a4txcv4h-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
# POSTGRES_PRISMA_URL="postgres://default:zQP9da1wetiY@ep-hidden-sun-a4txcv4h-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require&pgbouncer=true&connect_timeout=15"
# POSTGRES_URL_NO_SSL="postgres://default:zQP9da1wetiY@ep-hidden-sun-a4txcv4h-pooler.us-east-1.aws.neon.tech:5432/verceldb"
# POSTGRES_URL_NON_POOLING="postgres://default:zQP9da1wetiY@ep-hidden-sun-a4txcv4h.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require"
# POSTGRES_USER="default"
# POSTGRES_HOST="ep-hidden-sun-a4txcv4h-pooler.us-east-1.aws.neon.tech"
# POSTGRES_PASSWORD="zQP9da1wetiY"
# POSTGRES_DATABASE="verceldb"

# SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}/{os.environ['POSTGRES_DATABASE']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()