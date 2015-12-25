/**
 * Created by zach on 4/15/15.
 */
$(window).load(function() {
    doughnutWidget.options = {
        container: $('#container'),
        width: 100,
        height: 100,
        class: 'myClass',
        cutout: 50
    };

    doughnutWidget.render(data());

    setInterval(init, 2000);
});

function init() {
    doughnutWidget.render(data());
}

function data() {
    var data = {
        pending: {
            val: Math.round(Math.random() * 100),
            color: '#57B4F2',
            click: function(e) {
                console.log('hi');
            }
        },
        delivered: {
            val: Math.round(Math.random() * 100),
            color: '#6DED5C'
        },
        delayed: {
            val: Math.round(Math.random() * 100),
            color: '#E63329',
            link: 'http://www.google.com'
        }
    };

    return data;
}
