var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue2!',
        publications: [],
        categoryFilter: ['astro-ph', 'astro-ph.CO', 'astro-ph.EP', 'astro-ph.GA',
            'astro-ph.HE', 'astro-ph.IM', 'astro-ph.SR']
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
            let categories = ['CO', 'EP', 'GA', 'HE', 'IM', 'SR'];
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
        }
    },
    computed: {
        filteredPublications: function () {
            let filters = this.categoryFilter;
            return this.publications.filter(function (pub) {
                // loop all category filters
                for (let i in filters) {
                    if (pub.categories.includes(filters[i])) {
                        // filter in publication's list of categories
                        return true;
                    }
                }
                // nothing found
                return false;
            })
        }
    }
})