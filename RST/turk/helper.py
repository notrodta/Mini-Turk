from .models import DeveloperChosenForJob
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Profile
from .models import Profile, Job, Bidder, Message, JobSubmission

def get_lowest_bid(job):
    bid_list = job.bidder_set.all()
    count = job.bidder_set.count()

    if count > 0:
        lowest_bid = bid_list[0].price
        for bid in bid_list:
            if bid.price < lowest_bid:
                lowest_bid = bid.price
        job.lowest_bid = lowest_bid
        job.save()


def assign_developer(user, job, bidder_user, bidder, super_user, initial_payment):
    warn_cli(job)
    if(job.user.profile.warn_money == True):
        print('WARN MONEY == TRUE, return back')
        return
    bidder_user.profile.money += (initial_payment *.95)
    user.profile.money -= initial_payment
    super_user.profile.money += (initial_payment *.05)
    super_user.profile.save()
    bidder.isHired = True
    job.is_open = False
    job.save()
    bidder.save()
    bidder_user.profile.save()
    user.profile.save()
    developer = DeveloperChosenForJob(job=job, user=bidder_user)
    developer.save()

def give_trophy(profile):
    # Give trophy and revoke if they cant maintain

    # deliver before deadline and receive rating >=4 for >=5 demands, give early bird
    if((profile.num_early >= 5) and (profile.average_rating >=4)):
        profile.honor_Early_Bird = True
        profile.save()
    else:
        profile.honor_Early_Bird = False
        profile.save()

    # avg rating >=4 for >=10 demand, give hard worker
    if((profile.average_rating >=4) and (profile.rating_count >=10)):
        profile.honor_Hard_Worker = True
        profile.save()
    else:
        profile.honor_Hard_Worker = False
        profile.save()

    # made more than $1M from demands, give MILLIONAIRE!
    if(profile.money_earned > 1000000):
        profile.honor_MILLIONAIRE = True
        profile.save()

    # post >10 demands, give job supplier
    if(profile.num_post > 10):
        profile.honor_Job_Supplier = True
        profile.save()

    # dev worked on >=20 demands, give veteran
    if(profile.rating_count >= 20):
        profile.honor_Veteran = True
        profile.save()

    # clients got no bid on >10 expired demands, give toohardman
    if(profile.num_post_ex > 10):
        profile.honor_toohardman = True
        profile.save()

    # users with 'Tim' in name, give Cold-Headed-Tim
    if(profile.user.first_name == 'Tim'):
        profile.honor_Cold_Headed_Tim = True
        #print(profile.user.first_name)
        profile.save()
    else:
        profile.honor_Cold_Headed_Tim = False
        #print(profile.user.first_name)
        profile.save()

    # Get Age of Account
    a = timezone.now() - timezone.timedelta(hours=5) # -5 hrs b/c wrong timezone
    b = profile.acc_created
    c=a-b
    diff_day=c.days

    # >= 90 days, award Normie
    if(profile.honor_Novice == True):
        if(diff_day >= 90):
            # print('NORMIE')
            profile.honor_Novice = False
            profile.honor_Normie = True
            profile.save()

    # >= 365 days, award General
    if(profile.honor_Normie == True):
        if(diff_day >= 365):
            # print('GENERAL')
            profile.honor_Normie = False
            profile.honor.General = True
            profile.save()

    # 90+ days user + No activity, award Lurker
    if(diff_day >= 90):
        if(profile.rating_count == 0):
            profile.honor_Lurker = True
            profile.save()
        else:
            profile.honor_Lurker = False
            profile.save()


def warn_user(profile):
    # Poor Performance
    if(profile.rating_count >= 5):
        if(profile.average_rating <= 2):
            profile.warn_poor = True
            profile.save()

            # a = Message()
            # a.title = "Poor Performance"
            # a.message = "Your average rating is <= 2 for >= 5 projects"
            # a.user = profile.user
            # a.save()
        else:
            profile.warn_poor = False
            profile.save()

    # Irresponsible evaluations to others
    if(profile.rating_count >= 8):
        if((profile.avg_give_rating < 2) or (profile.avg_give_rating >4)):
            profile.warn_eval = True
            profile.save()

            # b = Message()
            # b.title = "Irresponsible Evaluations to Others"
            # b.message = "Your average rating to others is < 2 or >4 for >= 8 projects"
            # b.user = profile.user
            # b.save()
        else:
            profile.warn_eval = False
            profile.save()

    # # This part is outdated, moved to final_warn()
    # if((profile.warn_poor == True) and (profile.warn_eval == True) and (profile.warn_final == False)):
    #     profile.warn_final = True
    #     profile.save()
    #     print('Final warning:', profile.warn_final)

    # # Time to get tossed out :) for being warned twice hehexd
    # if(profile.warn_final == True):
    #     user.is_active = False
    #     user.save()
    #     profile.isBlackListed = True
    #     profile.save()
    #     print('byebye')

def ban(profile,user):
    if (profile.warn_final == True):
        user.is_active = False
        user.save()
        profile.isBlackListed = True
        profile.save()
        print('byebye')

def warn_cli(job):
    if(job.user.profile.money < job.job_price/2):
        # Give warning, close job
        job.user.profile.warn_money = True
        job.is_open = False
        job.is_complete = True
        print('Warned Client for being broke', job.user.profile.money, job.job_price/2)
        job.user.profile.save()
        job.save()

        # c = Message()
        # c.title = "Poor Client can't pay"
        # c.message = "You didn't have enough money to pay the developer."
        # c.user = profile.user
        # c.save()

def final_warn(profile):
    warning_count = 0
    if(profile.warn_eval == True):
        warning_count += 1
    if(profile.warn_poor == True):
        warning_count += 1
    if(profile.warn_money == True):
        warning_count += 1
    print('Warning Count: ', warning_count)
    if(warning_count >= 2):
        # Give Final Warning
        profile.warn_final = True
    else:
        profile.warn_final = False
    profile.save()


# def update_rate_db(rating, job):
#     job.user.profile.total_rating += rating
#     job.user.profile.rating_count += 1
#     job.user.profile.average_rating = (job.user.profile.total_rating / job.user.profile.rating_count)
#     job.user.profile.save()
#     job.is_rated = True
#     job.save()
#     print("job total rating: ", job.user.profile.total_rating)
#     print("job rating count: ", job.user.profile.rating_count)
#     print("job avereage rating: ", job.user.profile.average_rating)


def check_dev_late_proj_penalty(job, super_user):

    today_date = timezone.now() - timezone.timedelta(hours=5)  # -5 hrs b/c wrong timezone
    job_deadline = job.job_deadline
    c = job_deadline - today_date
    diff_seconds = c.seconds
    diff_days = c.days
    # print(c.days)
    # print("diff seconds: ",diff_seconds)
    # print("job_deadline: ", job_deadline)
    # print("today_date: ",today_date)
    #
    # print("asdaskdljasldjakkdj: ",job.job_title,diff_days,job.is_complete)

    # Overdue project, job isnt done
    if diff_days < 0 and job.is_complete == False:
        job.is_late = True
        job.is_complete = True
        client = job.user
        dev = job.developerchosenforjob.user

        print("Deadline past penalty!")
        print("dev money: ", dev.profile.money)
        print("client money: ", client.profile.money)
        print("admin money: ", super_user.profile.money)

        front_money = job.job_price/2
        penalty = 5
        dev.profile.money -= (front_money + penalty)
        client.profile.money += front_money
        super_user.profile.money += penalty

        rate(1, job, False)
        job.developerchosenforjob.is_rated = True

        print("dev money: ", dev.profile.money)
        print("client money: ", client.profile.money)
        print("admin money: ", super_user.profile.money)

        job.is_open = False
        job.save()
        client.profile.save()
        dev.profile.save()
        super_user.profile.save()


def rate(rating, job, isRatingClient):
    # Dev rates Client
    if isRatingClient:
        print("job.user.profile.total_rating: ", job.user.profile.total_rating)
        print("job.developerchosenforjob.user.profile.total_give_rating: ", job.developerchosenforjob.user.profile.total_give_rating)

        job.is_rated = True
        job.user.profile.total_rating += rating
        job.user.profile.rating_count += 1
        job.user.profile.average_rating = (job.user.profile.total_rating/ job.user.profile.rating_count)

        job.developerchosenforjob.user.profile.total_give_rating += rating
        job.developerchosenforjob.user.profile.total_give_count += 1
        job.developerchosenforjob.user.profile.avg_give_rating = (job.developerchosenforjob.user.profile.total_give_rating/job.developerchosenforjob.user.profile.total_give_count)

        print("job.user.profile.total_rating: ", job.user.profile.total_rating)
        print("job.developerchosenforjob.user.profile.total_give_rating: ", job.developerchosenforjob.user.profile.total_give_rating)

    # Client rates dev
    else:

        print("job.developerchosenforjob.user.profile.total_rating: ", job.developerchosenforjob.user.profile.total_rating)
        print("job.user.profile.total_give_rating: ", job.user.profile.total_give_rating)

        job.developerchosenforjob.is_rated = True
        job.developerchosenforjob.user.profile.total_rating += rating
        job.developerchosenforjob.user.profile.rating_count += 1
        job.developerchosenforjob.user.profile.average_rating = (job.developerchosenforjob.user.profile.total_rating/job.developerchosenforjob.user.profile.rating_count)

        job.user.profile.total_give_rating += rating
        job.user.profile.total_give_count += 1
        job.user.profile.avg_give_rating = (job.user.profile.total_give_rating/job.user.profile.total_give_count)

        print("job.developerchosenforjob.user.profile.total_rating: ", job.developerchosenforjob.user.profile.total_rating)
        print("job.user.profile.total_give_rating: ", job.user.profile.total_give_rating)

    job.user.profile.save()
    job.developerchosenforjob.user.profile.save()


def most_active_clients():
    most_active = Profile.objects.filter(position="Client").order_by('-rating_count')[:3]
    print("MOST ACTIVE: ", most_active)
    return most_active


def most_active_dev():
    most_active = Profile.objects.filter(position="Developer").order_by('-rating_count')[:3]
    print("MOST ACTIVE: ", most_active)
    return most_active


def most_money_made_dev():
    most_earned = Profile.objects.filter(position="Developer").order_by('-money_earned')[:3]
    print("MOST ACTIVE: ", most_earned)
    return most_earned


def total_num_clients():
    total = Profile.objects.filter(position="Client")
    return len(total)


def total_num_devs():
    total = Profile.objects.filter(position="Developer")
    return len(total)


