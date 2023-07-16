(function () {
  var jq_throttle;

  $.throttle = jq_throttle = function (
    delay,
    no_trailing,
    callback,
    debounce_mode
  ) {
    var timeout_id,
      last_exec = 0;

    // `no_trailing` defaults to falsy.
    if (typeof no_trailing !== "boolean") {
      debounce_mode = callback;
      callback = no_trailing;
      no_trailing = undefined;
    }

    function wrapper() {
      var that = this,
        elapsed = +new Date() - last_exec,
        args = arguments;

      // Execute `callback` and update the `last_exec` timestamp.
      function exec() {
        last_exec = +new Date();
        callback.apply(that, args);
      }

      // If `debounce_mode` is true (at_begin) this is used to clear the flag
      // to allow future `callback` executions.
      function clear() {
        timeout_id = undefined;
      }

      if (debounce_mode && !timeout_id) {
        // Since `wrapper` is being called for the first time and
        // `debounce_mode` is true (at_begin), execute `callback`.
        exec();
      }

      // Clear any existing timeout.
      timeout_id && clearTimeout(timeout_id);

      if (debounce_mode === undefined && elapsed > delay) {
        // In throttle mode, if `delay` time has been exceeded, execute
        // `callback`.
        exec();
      } else if (no_trailing !== true) {
        // In trailing throttle mode, since `delay` time has not been
        // exceeded, schedule `callback` to execute `delay` ms after most
        // recent execution.
        //
        // If `debounce_mode` is true (at_begin), schedule `clear` to execute
        // after `delay` ms.
        //
        // If `debounce_mode` is false (at end), schedule `callback` to
        // execute after `delay` ms.
        timeout_id = setTimeout(
          debounce_mode ? clear : exec,
          debounce_mode === undefined ? delay - elapsed : delay
        );
      }
    }

    // Set the guid of `wrapper` function to the same of original callback, so
    // it can be removed in jQuery 1.4+ .unbind or .die by using the original
    // callback as a reference.
    if ($.guid) {
      wrapper.guid = callback.guid = callback.guid || $.guid++;
    }

    // Return the wrapper function.
    return wrapper;
  };

  $.debounce = function (delay, at_begin, callback) {
    return callback === undefined
      ? jq_throttle(delay, at_begin, false)
      : jq_throttle(delay, callback, at_begin !== false);
  };


  $.fn.extend({
    slideBox: function(options) {
        if (options && typeof(options) == 'object') {
            options = $.extend({}, $.slideBox.defaults, options);
        }

        if($(this).length == 1) {
            new $.slideBox(this, options);
        } else if($(this).length > 1) {
            console.error($.messages.severalElements);
        } else if($(this).length == 0) {
            console.error($.messages.zeroElement);
        }

        return this;
    }
});

$.messages = {
    severalElements: '[jQuery.slideBox] Error: you have targetted more than one slideBox. Please use a different selector.',
    zeroElement: '[jQuery.slideBox] Error: could not find the slideBox in the DOM. Are you sure the selector is correct?'
};

$.closed = false;

$.position = {
    horizontal: null,
    vertical: null
};
// console.log($)

$.slideBox = function(elem, option) {
    var options  = option || $.slideBox.defaults
        , threShold = typeof(options.target) != 'number' ? $(options.target).offset().top : options.target;

    if($(elem).length === 1) {
        $.slideBox.applyCss(elem, options);

        $(window).on('scroll', function() {

            if($(this).scrollTop() + $(window).height() > threShold) {
                if(!$(elem).is(':visible') && !$(elem).is(':animated')) {
                    $.slideBox.showBox(elem, options);
                    $(elem).find(options.closeLink).on('click', function(e) {
                        e.preventDefault();
                        $.closed = true;
                        $.slideBox.hideBox(elem, options);
                    });
                }
            } else {
                if($(elem).is(':visible') && !$(elem).is(':animated')) {
                    $.slideBox.hideBox(elem, options);
                }
            }

        });
    }

    return;
};

$.slideBox.applyCss = function(elem, options) {
    var  position = options.position.split(' ')
        , cssPlacement = {}
        , propertiesNb
        , keys
        , value;

    $.position.vertical = position[0];
    $.position.horizontal = position[1];

    switch(position[0]) {
        case 'top':
            cssPlacement.top = 0;
            break;
        case 'middle':
            cssPlacement.top = '50%';
            cssPlacement.marginTop = parseInt($(elem).height()) / 2 * -1;
            break;
        case 'bottom':
            cssPlacement.bottom = 0;
            break;
    }

    switch(position[1]) {
        case 'left':
            cssPlacement.left = 0;
            break;
        case 'center':
            cssPlacement.left = '50%';
            cssPlacement.marginLeft = parseInt($(elem).width()) / 2 * -1;
            break;
        case 'right':
            cssPlacement.right = 0;
            break;
    }

    keys = Object.keys(cssPlacement);
    propertiesNb = keys.length;

    for(var i = 0; i < propertiesNb; i++) {
        $(elem).css(keys[i], cssPlacement[keys[i]]);
    }

    value = $.slideBox.calculateNewPosition(elem, options);
    $(elem).css(options.appearsFrom, value + 'px');

    $(elem).css({
        display: 'none',
        position: 'fixed'
    });

};

$.slideBox.hideBox = function(elem, options) {

    var animation = {};
    animation[options.appearsFrom] = $.slideBox.calculateNewPosition(elem, options);


    $(elem).animate(animation, {
        duration: options.slideDuration,
        complete: function() {
            $(elem).trigger('sb.hidden');
            $(elem).css('display', 'none');
        }
    });

};

$.slideBox.showBox = function(elem, options) {
    if(!$.closed) {

        $(elem).css('display', 'block');
        var animation = {}
            , value;

        switch(options.appearsFrom) {
            case 'top':
            case 'bottom':
                if($.position.vertical == options.appearsFrom) {
                    value = 0;
                } else {
                    value = $(window).innerHeight() - $(elem).outerHeight();
                }
                break;
            case 'left':
            case 'right':
                if($.position.horizontal == options.appearsFrom) {
                    value = 0;
                } else {
                    value = $(window).innerWidth() - $(elem).outerWidth();
                }
                break;
        }

        animation[options.appearsFrom] = value;
        $(elem).animate(animation, {
            duration: options.slideDuration,
            complete: function() {
                $(elem).trigger('sb.shown');
            }
        });
    }
};

$.slideBox.calculateNewPosition = function(elem, options) {
    var width = $(elem).outerWidth()
        , height = $(elem).outerHeight()
        , value;

    switch(options.appearsFrom) {
        case 'right':
        case 'left':
            value = width * -1;
            break;
        case 'top':
        case 'bottom':
            value = height * -1;
            break;
    }

    return value;
};

$.slideBox.defaults = {
    position: 'bottom right',
    appearsFrom: 'right',
    slideDuration: 1500,
    target: 1250,
    closeLink: null
};



  // $("#price-select").change($.debounce(1, false, setPrice));
  $("#price-select").change(setPrice);
  // $("#price-conform").click($.debounce(1000, false, setPrice));
  $("#price-conform").click(setPrice);


  

  function setPrice() {
    var price = $("#price-select").val();
    var price1 = $("#price-input").val();

    if (price == "" && price1 == "") {
      // alert("price not select");
      return;
    }
    if (isNaN(Number(price))) {
      alert("not number price");
      return;
    }
    if (isNaN(Number(price1))) {
      alert("not number price1");
      return;
    }

    var selectedPrice = price ? price : price1;

    if (
      selectedPrice != "" &&
      selectedPrice != null &&
      selectedPrice != undefined
    ) {
      $.ajax({
        method: "POST",
        url: base_url + "contribute/change-price",
        data: {
          price: selectedPrice,
        },
        success: function (res) {
          if (res == 1) {
            window.location.reload();
          }
        },
      });
    }
  }


  $("#not-interested").click(function(){
    localStorage.setItem("notification", "hide");
    $("#slidebox").hide(200);
    window.location.reload();
  })

  


  
  if(localStorage.getItem('notification') == null){
    $('#slidebox').slideBox({
        position: 'middle', // can be [bottom|middle|top] and [left|center|right]
        appearsFrom: 'bottom', // can be [left|top|right|bottom]
        slideDuration: 300, // animation duration in ms
        target: '#target-div-notification', // can be a string (jQuery selector) or an offset (in px)
        closeLink: '#close' // a string that is the jQuery selector of the closing element
    }).on('sb.hidden', function() {
        console.log('hidden');
        // localStorage.setItem("notification", "hide");
    }).on('sb.shown', function() {
        console.log('shown');
    });
  }

  
})();
