const accountTypes = document.getElementsByClassName("account-wrapper")[0].children;
for (let i of accountTypes) {
    i.firstElementChild.addEventListener("click", function(e) {
        e.target.parentNode.setAttribute("id", "selected");
        for (let j of accountTypes) {
            if (j === e.target.parentNode) continue;
            j.setAttribute("id", "not-selected");
        }
    })
}