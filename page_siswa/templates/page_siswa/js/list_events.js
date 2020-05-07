document.addEventListener('DOMContentLoaded', function () {
    var initialLocaleCode = 'id';
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
      plugins: ['dayGrid'],
      height: 'parent',
      header: {
        left: 'prev,next',
        center: 'title',
        right: 'dayGridMonth'
      },
      defaultDate: '2020-02-12',
      locale: initialLocaleCode,
      buttonIcons: false, // show the prev/next text
      weekNumbers: false,
      navLinks: false, // can click day/week names to navigate views
      editable: false,
      eventLimit: false, // allow "more" link when too many events
      events: [
        {% for event in events%}
            {
            title: '{{event.name}}',
            start: '{{event.start_date|safe}}',
            end: '{{event.end_date|safe}}',
            classNames: ['bg-dark']
            },
        {% endfor %}
      ],
    });

    calendar.render();

  });