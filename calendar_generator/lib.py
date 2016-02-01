from datetime import date, timedelta
import calendar

def get_days(calendar):
    out = {}
    
    skip_days = set()
    reset_days = {}
    day_rotation = []
    
    for day in calendar.day_set.all():
        day_rotation.append(day)
    
    for skipdate in calendar.skipdate_set.all():
        skip_days.add(skipdate.date)
        
        if skipdate.end_date:
            working_date = skipdate.date
            
            while working_date <= skipdate.end_date:
                skip_days.add(working_date)
                working_date += timedelta(days=1)
    
    for resetdate in calendar.resetdate_set.all():
        reset_days[resetdate.date] = resetdate.day
    
    day_counter = 0
    
    out[calendar.start_date] = day_rotation[day_counter % len(day_rotation)]
    
    working_date = calendar.start_date
    while working_date < calendar.end_date:
        working_date += timedelta(days=1)
        weekday = working_date.weekday()
        
        #Skip any unselected days
        if not calendar.monday and weekday == 0:
            continue
        
        if not calendar.tuesday and weekday == 1:
            continue
        
        if not calendar.wednesday and weekday == 2:
            continue
        
        if not calendar.thursday and weekday == 3:
            continue
        
        if not calendar.friday and weekday == 4:
            continue
        
        if not calendar.saturday and weekday == 5:
            continue
        
        if not calendar.sunday and weekday == 6:
            continue
        
        if working_date in skip_days:
            continue
        
        #Bump day here since we've already bumped the working date
        day_counter += 1
        
        #If we're resetting, we bump the counter back to this number - since it gets
        #Rotated, it doesn't have to be continuious
        if working_date in reset_days:
            day_counter = day_rotation.index(reset_days[working_date])
        
        out[working_date] = day_rotation[day_counter % len(day_rotation)]
        
    return out

def get_monday(d):
    return d - timedelta(days=d.weekday())

def get_friday(d):
    return get_monday(d) + timedelta(days=4)

def custom_range_grid(days, calendar_from, calendar_to):
    if calendar_from >= calendar_to:
        raise ValueError("To date must be after from date")
    
    out = []
    
    #Since the data needs to be strucutred by week, we iterate up the Mondays
    #and then what needs to be in them
    working_monday = get_monday(calendar_from)
    
    while working_monday <= calendar_to:
        week = []
        out.append(week)
        
        for i in range(7):
            working_date = working_monday + timedelta(days=i)
            if calendar_from <= working_date <= calendar_to:
                #This date should be in there
                day = days.get(working_date)
                week.append((working_date, day))
            else:
                week.append(None)
        
        working_monday += timedelta(days=7)
    
    return out

#Spits out the calendar as a 2d list, indexed by the year and month    
def structured_calendar_layout(days, prefill_calendar=False, postfill_calendar=False):
    out = {}
    
    first_day = min(days)
    last_day = max(days)
    
    months = set()
    
    for day in days:
        months.add((day.year, day.month))
    
    for year, month in months:
        calendar_grid = calendar.monthcalendar(year, month)
        for week in calendar_grid:
            reference_day = max(week)
            reference_date = date(year, month, reference_day)
            reference_index = week.index(reference_day)
            
            #First loop - put datetime objects into the week list
            #for any dates that should be shown (taking into account backfill and forwardsfill)
            for i, day in enumerate(week):
                if day:
                    week[i] = date(year, month, day)
                else:
                    delta = i - reference_index
                    day = reference_date + timedelta(days=delta)
                    
                    #Date object in the week list has gone back a month
                    if prefill_calendar and ((day.year, day.month) < (reference_date.year, reference_date.month)):
                        week[i] = day
                    
                    #Date object in the week list has gone forwards a month
                    elif postfill_calendar and ((day.year, day.month) > (reference_date.year, reference_date.month)):
                        week[i] = day
                    
                    #We're not filling this particular date
                    else:
                        week[i] = None
            
            #We're enumerating twice for my sanity
            #Second loop - transform the date objects into (date, letter) tuples
            for i, day in enumerate(week):
                if day:
                    week[i] = (day, days.get(day))
        
        def work_week_in_month(week, year, month):
            for item in week:
                if item and item[0].year == year and item[0].month == month:
                    return True
                    
            return False
            
        calendarGrid = [week[0:5] for week in calendar_grid if work_week_in_month(week[0:5], year, month)]
        
        out[(year, month)] = calendar_grid

    return out