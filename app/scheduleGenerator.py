from operator import itemgetter
from datetime import datetime, timedelta

def schedule_tasks(task_list, allocated_time):
    # print(task_list)
    # print(allocated_time)
    # Sort tasks by priority
    sorted_tasks = sorted(task_list, key=itemgetter('priority'))
    # print(sorted_tasks)

    # Convert time strings to datetime objects for easier comparison
    for slot in allocated_time:
        slot['start'] = datetime.strptime(slot['start'], '%I:%M %p')
        slot['end'] = datetime.strptime(slot['end'], '%I:%M %p')
    # print(allocated_time)
    scheduled_tasks = []

    for task in sorted_tasks:
        # Set task duration based on priority
        if task['priority'] == 1:
            task_duration = timedelta(hours=1)
        elif task['priority'] == 2:
            task_duration = timedelta(minutes=30)
        elif task['priority'] == 3:
            task_duration = timedelta(minutes=15)
        else:
            task_duration = timedelta(minutes=5)

        # Iterate over available time slots to find a suitable slot for the task
        for slot in allocated_time:
            slot_start = slot['start']
            slot_end = slot['end']

            if slot_start <= slot_end:
                task_start = slot_start
                task_end = task_start + task_duration
                if task_end <= slot_end:
                    scheduled_tasks.append({
                        'name': task['name'],
                        'start': task_start.strftime('%I:%M %p'),
                        'end': task_end.strftime('%I:%M %p'),
                        'priority':task['priority']
                    })
                    slot['start'] = task_end  # Update start time of the slot
                    break

    return scheduled_tasks


if __name__=="__main__":
    # task_list = [
    #     {"name":"exercise", "priority":1},
    #     {"name":"play games", "priority":4},
    #     {"name":"fill up job application form","priority":2},
    #     {"name": "call your friend, to ask about next episode in serial","priority":3}
    # ]

    import random

    task_list = []

    # Generate around 30 sample tasks
    for i in range(30):
        task_name = f"Task {i+1}"
        priority = random.randint(1, 4)
        task_list.append({"name": task_name, "priority": priority})

    # print(task_list)


    allocated_time = [
        {"start":"12:30 AM","end":"3:00 AM"},
        {"start":"9:30 AM","end":"10:00 AM"},
        {"start":"8:30 AM","end":"11:00 AM"},
        {"start":"12:30 PM","end":"12:45 PM"},
        {"start":"12:40 PM","end":"12:50 PM"},
    ]

    scheduled_tasks = schedule_tasks(task_list, allocated_time)
    for task in scheduled_tasks:
        print(task)
