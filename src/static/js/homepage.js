(function() {
        
  // state
  var isMultiFieldQueryActive = false

  // dropdown-toggle
  const closeRef = document.getElementById("multi-field-query-close")
  const toggleRef = document.getElementById("multi-field-query-action")
  const dropdownRef = document.getElementById("multi-field-query-dropdown")

  // search-box
  const mainQueryRef = document.getElementById("main_query")

  // input-fields
  const inputTitleRef = document.getElementById("pub_title")
  const inputAuthorRef = document.getElementById("pub_author")
  const inputCategoryRef = document.getElementById("pub_category")

  function bindMultiFieldQuery() {
    if (isMultiFieldQueryActive) {
      dropdownRef.classList.add("active")

      mainQueryRef.removeAttribute("name") 
      mainQueryRef.setAttribute("disabled", "disabled")
      
      inputTitleRef.setAttribute("name", "title")
      inputAuthorRef.setAttribute("name", "author")
      inputCategoryRef.setAttribute("name", "category")
    } else {
      dropdownRef.classList.remove("active")

      mainQueryRef.setAttribute("name", "q")
      mainQueryRef.removeAttribute("disabled") 

      inputTitleRef.removeAttribute("name")
      inputAuthorRef.removeAttribute("name")
      inputCategoryRef.removeAttribute("name")
    }
  }

  closeRef.onclick = function() {
    isMultiFieldQueryActive = false
    bindMultiFieldQuery()
  }

  toggleRef.onclick = function() {
    isMultiFieldQueryActive = true
    bindMultiFieldQuery()
  }

})();
