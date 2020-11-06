var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue2!',
        publications: [],
        categoryFilter: []
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
        },
        toggleAstroPhFilter: function () {
            let checked = this.categoryFilter.includes('astro-ph');
            let categories = ['co', 'ep', 'ga', 'he', 'im', 'sr'];
            for (let c in categories) {
                let cat = 'astro-ph.' + categories[c];
                if (checked && !this.categoryFilter.includes(cat)) {
                    this.categoryFilter.push(cat);
                }
                if (!checked && this.categoryFilter.includes(cat)) {
                    this.categoryFilter = this.categoryFilter.filter(
                        function (value, index, arr) {
                            return value != cat;
                        });
                }
            }
            this.applyFilter();
        },
        applyFilter: function () {
            console.log('filter');
        }
    },
    computed: {
        filteredPublications: function () {
            return this.publications.filter(function (pub) {
                return pub.title.includes('Disk');
            })
        }
    }
})