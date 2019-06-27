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

function getReplyTable(node) {
    for( ; node && node !== document; node = node.parentNode ) {
        if (node.tagName === "TABLE") {
            return node.parentNode.children[1];
        }
    }
    return null;
}

function toggle(event, node) {
    var isCollapsed = node.getAttribute('data-collapsed');
    var replyTable = getReplyTable(node);
    if (isCollapsed === "false") {
        node.setAttribute('data-collapsed', 'true');
        node.innerText = '[+]';
        replyTable.style.display = 'none';
    } else {
        node.setAttribute('data-collapsed', 'false');
        node.innerText = '[-]';
        replyTable.style.display = '';
    }
}