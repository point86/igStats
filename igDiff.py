import pickle
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="A simple python utility that shows the difference between 2 igStats's followers dumps. Useful to spot who unfollowed you.")
    parser.add_argument("file1",  help="Oldest igStats dump")
    parser.add_argument("file2",  help="Newer  igStats dump")
    args = parser.parse_args()

    f1 = args.file1
    f2 = args.file2
  
    (t1, s1) = pickle.load(open(f1, "rb"))
    (t2, s2) = pickle.load(open(f2, "rb"))

    t1 = time.strftime('%d %b %Y - %l:%M%p', time.gmtime(t1))
    t2 = time.strftime('%d %b %Y - %l:%M%p', time.gmtime(t2))

    print(f"Between {t1} and {t2}, those profiles unfollowed you:")
    unf = s2-s1
    for u in unf:
        print(f"{u}", end = ", ")
    print("\b\b;\n=========================")

if __name__ == '__main__':
    main()