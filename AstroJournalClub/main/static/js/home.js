var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue2!',
        publications: []
    },
    created: function () {
        // take publications
        this.publications = publications;
    },
    methods: {
        vote: function (pub, updown) {
            // get date and URL
            let date = pub.date.replace(/-/g, '/');
            let url = '/api/' + date + '/' + pub.identifier + '/vote';

            // do request
            this.$http.get(url).then(function (response) {
                // set from response
                let b = response.body;
                pub.votes = b.votes;
                pub.has_voted = b.has_voted;
            }, function (response) {
                alert("Error on vote");
            });
        }
    }
})