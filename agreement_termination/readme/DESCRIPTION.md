This module adds the "Term Dates" section to legal agreements, grouping the
signature/start/end dates together with the expiration and change notice
periods, the notification address and the termination tracking dates
(termination requested / terminated).

It also adds a review date to each agreement, computed as the end date minus
the expiration notice. A daily cron schedules a "review" activity on that date,
assigned to the user who last modified the agreement.

![Agreement Form](../static/description/screenshot_form.png)