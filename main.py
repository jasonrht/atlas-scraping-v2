import rotterdam as rtm
import amsterdam as ams
import nijmegen as nmg
import apeldoorn as apd
import utrecht as utr
import send_mail as sm
import datetime as dt

def main():
    t0 = dt.datetime.now()
    print(t0)

    rtm.main()
    ams.main()
    nmg.main()
    apd.main()
    utr.main()

    sm.send_m('jtsangsolutions@gmail.com',[''])

    t1 = dt.datetime.now()
    print(f'Script run in {t1-t0}')

if __name__ == '__main__':
    main()