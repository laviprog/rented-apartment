function showContent(contentId) {
    var contents = document.querySelectorAll('.content');
    contents.forEach(function(content) {
        content.style.display = 'none';
    });

    var contentToShow = document.getElementById(contentId);
    contentToShow.style.display = 'block';
}