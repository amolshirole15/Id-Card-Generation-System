Sub CreateProjectPresentation()
    ' Create PowerPoint application and presentation
    Dim pptApp As Object
    Dim pptPresentation As Object
    Dim slide As Object
    Set pptApp = CreateObject("PowerPoint.Application")
    pptApp.Visible = True
    Set pptPresentation = pptApp.Presentations.Add

    ' Slide 1: Title Slide
    Set slide = pptPresentation.Slides.Add(1, 1)
    slide.Shapes.Title.TextFrame.TextRange.Text = "Django Project Presentation"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = "A showcase of main features and implementation"

    ' Slide 2: Project Overview
    Set slide = pptPresentation.Slides.Add(2, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "Project Overview"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = "This project is built using Django, implementing key functionalities such as user registration, profile management, and ID card generation."

    ' Slide 3: Main Features
    Set slide = pptPresentation.Slides.Add(3, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "Main Features"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = _
        "- User Registration and Profile Management" & vbCrLf & _
        "- ID Card Generation with QR Codes" & vbCrLf & _
        "- Customizable Templates for Organizations"

    ' Slide 4: User Registration and Profile Update
    Set slide = pptPresentation.Slides.Add(4, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "User Registration and Profile Update"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = _
        "Allows users to register and update profiles with validation checks on fields like organization code and password confirmation."

    ' Slide 5: Form Validations
    Set slide = pptPresentation.Slides.Add(5, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "Form Validations"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = _
        "- Password confirmation checks" & vbCrLf & _
        "- Unique organization code validation" & vbCrLf & _
        "- Conditional fields for new vs. updating profiles"

    ' Slide 6: ID Card Generation
    Set slide = pptPresentation.Slides.Add(6, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "ID Card Generation"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = _
        "Multiple templates available for generating ID cards, complete with QR codes and user details. Organizations can select custom templates."

    ' Slide 7: Screenshots
    Set slide = pptPresentation.Slides.Add(7, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "Project Screenshots"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = "Add screenshots of user registration, profile update forms, and generated ID cards here."

    ' Slide 8: Conclusion and Future Enhancements
    Set slide = pptPresentation.Slides.Add(8, 2)
    slide.Shapes.Title.TextFrame.TextRange.Text = "Conclusion and Future Enhancements"
    slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = _
        "Future ideas include more ID card customization, integration with more databases, and enhancing the user interface."

    ' Cleanup
    Set slide = Nothing
    Set pptPresentation = Nothing
    Set pptApp = Nothing

    MsgBox "Presentation created successfully!"
End Sub
