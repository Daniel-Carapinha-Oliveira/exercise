document.addEventListener("DOMContentLoaded", () => {
  // Select elements
  const muscleGroupSelect = document.getElementById("id_muscle_group");
  const muscleSelect = document.getElementById("id_muscle");
  const musclePartSelect = document.getElementById("id_muscle_part");

  // selected values in select elements
  const selectedMuscleGroup = muscleGroupSelect.value || null;
  const selectedMuscle = muscleSelect.value || null;
  const selectedMusclePart = musclePartSelect.value || null;

  // function to set a placeholder on a select element and its disabled state
  function setSelectElementPlaceholder(element, message, disabled_state = true) {
    /*
    element: the element to be altered;
    message: the placeholder to set on the element option
    disabled_state: true or false, to define the element state
    */
    element.innerHTML = `<option value="">${message}</option>`;
    element.disabled = disabled_state;
  }

  // --- Load muscles for selected muscle group ---
  function loadMuscles(MuscleGroupId, selectedMuscleId = null) {
    if (!MuscleGroupId) {
      setSelectElementPlaceholder(muscleSelect, "Choose a muscle group first");
      setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");
      return;
    }

    setSelectElementPlaceholder(muscleSelect, "Loading...", true);

    fetch(`/api/muscles/?muscle_group=${MuscleGroupId}`)
      .then(res => res.json())
      .then(data => {
        if (data.length === 0) {
          setSelectElementPlaceholder(muscleSelect, "None available");
          setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");
          return;
        }

        muscleSelect.disabled = false;
        muscleSelect.innerHTML = ""; // clear previous options

        const defaultOption = new Option("Not selected", "");
        muscleSelect.appendChild(defaultOption);

        data.forEach(m => {
          const option = new Option(m.name, m.id);
          if (selectedMuscleId && selectedMuscleId == m.id) {
            option.selected = true;
          }
          muscleSelect.appendChild(option);
        });
      })
      .catch(() => {
        setSelectElementPlaceholder(muscleSelect, "Error loading muscles");
        setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");
      });
  }

  // --- Load muscle parts for selected muscle ---
  function loadMuscleParts(muscleId, selectedPartId = null) {
    if (!muscleId) {
      setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");
      return;
    }

    setSelectElementPlaceholder(musclePartSelect, "Loading...", true);

    fetch(`/api/muscle-parts/?muscle=${muscleId}`)
      .then(res => res.json())
      .then(data => {
        if (data.length === 0) {
          setSelectElementPlaceholder(musclePartSelect, "None available");
          return;
        }

        musclePartSelect.disabled = false;
        musclePartSelect.innerHTML = ""; // clear previous options

        const defaultOption = new Option("Not selected", "");
        musclePartSelect.appendChild(defaultOption);

        data.forEach(mp => {
          const option = new Option(mp.name, mp.id);
          if (selectedPartId && selectedPartId == mp.id) {
            option.selected = true;
          }
          musclePartSelect.appendChild(option);
        });
      })
      .catch(() => {
        setSelectElementPlaceholder(musclePartSelect, "Error loading muscle parts");
      });
  }

  // Event handlers for changes in filter choices
  muscleGroupSelect.addEventListener("change", () => {
    // insert placeholder in muscle part
    setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");

    const MuscleGroupId = muscleGroupSelect.value;
    loadMuscles(MuscleGroupId);
  });

  muscleSelect.addEventListener("change", () => {
    const muscleId = muscleSelect.value;
    loadMuscleParts(muscleId);
  });

  // refresh values
  if (selectedMuscleGroup) {
    loadMuscles(selectedMuscleGroup, selectedMuscle);
    if (selectedMuscle) {
      loadMuscleParts(selectedMuscle, selectedMusclePart);
    } else {
      setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");
    }
  } else {
    setSelectElementPlaceholder(muscleSelect, "Choose a muscle group first");
    setSelectElementPlaceholder(musclePartSelect, "Choose a muscle first");
  }
});
