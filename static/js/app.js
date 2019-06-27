function parseCrsfToken() {
    let token = '';
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function (c) {
            var m = c.trim().match(/(\w+)=(.*)/);
            if (m !== undefined && m[1] === 'csrftoken') {
                token = decodeURIComponent(m[2]);
            }
        });
    }
    return token;
}

var crsfToken = parseCrsfToken();

function upvote(item, item_str) {
    let id = item.id.substring(3);

    let data = {id: id};
    let url = ((item_str === 'post') ? '/upvote-post' : '/upvote-comment');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': crsfToken
        },
        body: JSON.stringify(data)
    }).then(res => {

        res.json().then(res => {
            if (res.success) {
                item.children[0].style.visibility = 'hidden';

                scoreItem = document.getElementById('score_' + id);
                if (item_str === 'post') {
                    scoreItem.innerText =
                        (parseInt(scoreItem.innerText.match(/\d+/)[0]) + 1).toString() + ' points';
                }
            } else if (res.redirect) {
                window.location = '/accounts/login';
            }
        })

    }).catch(error => console.log(error));
}

function upvotePost(item) {
    upvote(item, 'post')
}

function upvoteComment(item) {
    upvote(item, 'comment')
}

function noshow (el) { if (el) { el.classList.add('noshow'); } }
function elShow (el) { if (el) { el.classList.remove('noshow'); } }
function vis(el, on) { if (el) { on ? el.classList.remove('nosee') : el.classList.add('nosee'); } }

function ind(el) { if (el) { return (el.getElementsByTagName('img')[0] || { width: 0 }).width; } }
function aeach(fn, a) { return Array.prototype.forEach.call(a, fn); }
function acut(a, m, n) { return Array.prototype.slice.call(a, m, n); }

function allof(cls) { return document.getElementsByClassName(cls); }
function allcomments() { return allof('comtr'); }
function allcollapsed() { return allof('coll'); }

function posf (f, a) { for (var i=0; i < a.length; i++) { if (f(a[i])) return i; } return -1; }
function apos (x, a) { return (typeof x == 'function') ? posf(x,a) : Array.prototype.indexOf.call(a,x) }
function afind (x, a) { var i = apos(x, a); return (i >= 0) ? a[i] : null; }

function toggle(ev, id) {
    var node = document.getElementById(id);
    var isCollapsed = afind(node, allcollapsed());
    isCollapsed ? node.classList.remove('coll') : node.classList.add('coll');
    recollapse();
    ev.stopPropagation();
    return false;
}

function expand(tr) {
    elShow(tr);
    elShow(tr.querySelector('.comment'));
    vis(tr.querySelector('.votelinks'), true);
    tr.querySelector('.togg').innerHTML = '[-]';
}

function kidsOf(id) {
    var kids = [];
    var comments = allcomments();
    var node = document.getElementById(id);
    var i = apos(node, comments);
    if (i >= 0) {
        kids = acut(comments, i+1);
        var n = ind(node);
        var j = apos(function(tr) { return ind(tr) <= n }, kids);
        if (j >= 0) { kids = acut(kids, 0, j); }
    }
    return kids;
}

function squish(tr) {
    if (tr.classList.contains('noshow')) {
        return;
    }
    aeach(noshow, kidsOf(tr.id));
    var toggle = tr.querySelector('.togg');
    toggle.innerHTML = '[+'+ (getChildrenCount(tr.id) + 1) +']';
    noshow(tr.querySelector('.comment'));
    vis(tr.querySelector('.votelinks'), false);
}

function recollapse() {
    var comments = allcomments();
    aeach(expand, comments);

    var collapsed = allcollapsed();
    aeach(squish, collapsed);
}

function getChildrenCount(id) {
    return kidsOf(id).length;
}