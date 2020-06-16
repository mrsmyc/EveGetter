window.onload=function(){
  $(document).ready(function() {
    $(".ch_search").chosen();
    $(".popup").magnificPopup();
  });

  $(document).ready(function(){
    $('input.timepicker').flatpickr({
      enableTime: true,
      noCalendar: true,
      dateFormat: "H:i",
      defaultDate: "13:45",
      time_24hr: true,
      timeFormat: "H:i:s"
    });
  });

  $(document).ready(function(){
    $('input.id_event_date').flatpickr({
      dateFormat: 'd.m.Y',
      locale: {
        firstDayOfWeek: 1,
        weekdays: {
          shorthand: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
          longhand: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],         
        }, 
        months: {
          shorthand: ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
          longhand: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        },
      },
    });
  });
  
  $(document).ready(function(){
    $('#id_event_date').flatpickr({
      dateFormat: 'd.m.Y',
      locale: {
        firstDayOfWeek: 1,
        weekdays: {
          shorthand: ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'],
          longhand: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],         
        }, 
        months: {
          shorthand: ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
          longhand: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
        },
      },
    });
  });
  let show = document.getElementById('post_comment');
  let PostComment = document.getElementById('comment_post_showup');
  if (show !== null) {
    show.addEventListener("click", () =>{
      PostComment.style.display = "block";
    }); 
  };
  
  //AJAX comments pagination
  
  function ajaxCommentsPagination() {
    $('#pagination_comments_1 a.page-link').each((index, el)=>{
      $(el).click((e)=>{
        e.preventDefault()
        let page_url = $(el).attr('href')
  
        $.ajax({
          url: page_url,
          type: 'GET',
          success: (data)=>{
            $('#reviews_div').empty()
            $('#reviews_div').append( $(data).find('#reviews_div').html())
  
            $('#pagination_comments_1').empty()
            $('#pagination_comments_1').append( $(data).find('#pagination_comments_1').html())
          }
        })
      })
    })
  }
  
  $(document).ready(function(){
    ajaxCommentsPagination()
  })
  
  $(document).ajaxStop(function(){
    ajaxCommentsPagination()
  })
}

// $(document).ready(function(){
//   $('input.timepicker').timepicker({});
// });

// $(document).ready(function(){
//   $('input.id_event_date').flatpickr({});
// });

// Тестирую ajax поиск в моих мероприятиях

// const user_input = $("#user-input")
// const search_icon = $('#search-icon')
// const artists_div = $('#replaceable-content')
// const endpoint = '/myevents2/'
// const delay_by_in_ms = 700
// let scheduled_function = false

// let ajax_call = function (endpoint, request_parameters) {
// 	$.getJSON(endpoint, request_parameters)
// 		.done(response => {
// 			// fade out the artists_div, then:
// 			artists_div.fadeTo('slow', 0).promise().then(() => {
// 				// replace the HTML contents
// 				artists_div.html(response['html_from_view'])
// 				// fade-in the div with new contents
// 				artists_div.fadeTo('slow', 1)
// 				// stop animating search icon
// 				// search_icon.removeClass('blink')
// 			})
// 		})
// }


// user_input.on('keyup', function () {

// 	const request_parameters = {
// 		q: $(this).val() // value of user_input: the HTML element with ID user-input
// 	}

// 	// start animating the search icon with the CSS class
// 	search_icon.addClass('blink')

// 	// if scheduled_function is NOT false, cancel the execution of the function
// 	if (scheduled_function) {
// 		clearTimeout(scheduled_function)
// 	}

// 	// setTimeout returns the ID of the function to be executed
// 	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
// })

































































