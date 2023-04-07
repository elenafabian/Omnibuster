//--------------- highlight text ----------------------------
function highlightSelection() {   

  // MY WORK: trying to make it be in separate spans; cant figure out how to iterate

  /*
  let selection= window.getSelection().getRangeAt(0);

  console.log(selection)

  // BEGIN HGHLIGHTED SECTION
  console.log(selection.startContainer.tagName)
  text = selection.startContainer.parentElement.innerHTML;
  start = selection.startOffset;
  end = text.length;

  if (selection.startContainer == selection.endContainer) {
    end = selection.endOffset;
  }

  console.log(text.slice(0, start))
  console.log(text.slice(start, end))
  selection.startContainer.parentElement.innerHTML = text.slice(0, start) +
                                                    "<span style=\"background-color: yellow;\">" + 
                                                    text.slice(start, text.length) + "</span>";
  


  let ancestor = selection.commonAncestorContainer
 */
  
  let selection= window.getSelection().getRangeAt(0);
  // check here
  let selectedContent = selection.extractContents();
  var span= document.createElement("span");
  span.style.backgroundColor = "#ffff88";
  span.appendChild(selectedContent);
  selection.insertNode(span);
  
}

//--------------- open/close toc pane ----------------------------
function openNav() {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "300px";
  document.getElementById("commPane").style.width= "300px";
  document.getElementById("highlightBtn").style.right = "310px";
  //document.getElementById("mySidenav").style.overflowY = "hidden";
  document.getElementById("myNavContainer").style.display = "contents";
  document.getElementById("openbtn").style.display = "none";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "50px";
  document.getElementById("main").style.marginLeft= "100px";
  document.getElementById("commPane").style.width= "500px";
  document.getElementById("highlightBtn").style.right = "510px";
  //document.getElementById("mySidenav").style.overflowY = "show";
  document.getElementById("myNavContainer").style.display = "none";
  document.getElementById("openbtn").style.display = "block";
}

//--------------- jump to section ----------------------------

// TODO: align correctly
function tocLinkScript() {
  // source: https://codemyui.com/sticky-sidebar-navigation-on-scroll/

  let mainNavLinks = document.querySelectorAll("nav div a"); // includes all navbar links as elements
  let mainSections = document.querySelectorAll("main div div"); // includes all section header lines in text body as elements

  let lastId;
  let cur = [];

  // This should probably be throttled.
  // Especially because it triggers during smooth scrolling.
  // https://lodash.com/docs/4.17.10#throttle
  // You could do like...
  // window.addEventListener("scroll", () => {
  //    _.throttle(doThatStuff, 100);
  // });
  // Only not doing it here to keep this Pen dependency-free.

  window.addEventListener("scroll", event => {
    let fromTop = window.scrollY;
    mainNavLinks.forEach(link => {
      let section = document.querySelector(link.hash);
      if (section.offsetTop <= fromTop && section.offsetTop + section.offsetHeight > fromTop) {
        link.classList.add("current");
      } 
      else {
        link.classList.remove("current");
      }
    });
  })
}

//--------------- commenting ----------------------------

// TODO: 
// idea: when you click on the comment pane and type, we get the y-coord or line number? of the nearest text and save the comment at that place so when you scroll it appears there
// easier idea: comments aren't actually tied to text but that would be less useful

function saveComment() {
  // get the current text in the comment box
  var textArea = document.getElementById("rawComm");
  input = textArea.value;
  // get the current date
  var date = new Date();
  var year = date.getFullYear();
  var month = date.getMonth();
  var day = date.getDay();
  var hour = date.getHours();
  var min = date.getMinutes();
  var dateString = "<span class=\"dateComm\">" + month + "/" + day + "/" + year + "@" + hour + ":" + min + "</span>";
  // create the new comment
  var newComm = "<div class=\"savedComm\">" + dateString + input + "</div>"
  // append new comment to pane
  var commPane = document.getElementById("commPane");
  commPane.innerHTML += newComm;

  // ALTERNATIVE: ALSO WRITE BACK TO DOC WITH AJAX
  // THEN IN omnibusterDOM.PY WE'LL READ FROM THAT DOCUMENT

  // reset the comment box to accept a new comment
  textArea.value = "Add new comment..."
  return;
}


//--------------- collapsible sections -------------------
function collapsibleScript() {
var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }
}

//--------------- start scripts -------------------
collapsibleScript();
tocLinkScript();
