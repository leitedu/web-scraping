Attribute VB_Name = "Report"
Sub relatorio()

'Define variables
Dim start, obj As Integer
Dim cell As Range

'Define Outlook
Dim olk As outlook.Application
Dim email As outlook.MailItem

'Handles Presentation
Set PPT = CreateObject("PowerPoint.Application")
Set file = PPT.Presentations.Open(Sheets("Parameters").Range("C2").Value) 'Opens presentaion model
Set cover = file.Slides(1)

Sheets("Filling table").Select 'Sheet that controls slides and contents

'Loop for each informtion added to the report
For Each cell In Range(Range("B3"), Range("B3").End(xlDown))

    Set slide = file.Slides(cell.Offset(0, 2).Value) 'Finds slide where informtion will be displayed
    slide.Select
    
    If cell.Offset(0, -1).Value = "T" Then 'Text content
        Set form = slide.Shapes(cell.Offset(0, 7).Value)
        start = form.TextFrame.TextRange.Find(cell.Offset(0, 3).Value).Characters.Start
        form.TextFrame.TextRange.Characters(start).InsertBefore (cell.Offset(0, 4).Value)
        form.TextFrame.TextRange.Find(cell.Offset(0, 3).Value).Delete

    
    ElseIf cell.Offset(0, -1).Value = "S" Then 'Image content
        Sheets(cell.Offset(0, 5).Value).Range(cell.Offset(0, 3).Value) = cell.Offset(0, 4).Value
        Sheets(cell.Offset(0, 5).Value).Range(cell.Offset(0, 6).Value).CopyPicture Appearance:=xlScreen, formt:=xlPicture
        slide.Shapes.Paste
        obj = cell.Offset(0, 7).Value
        With slide.Shapes.Range(obj)
            .ScaleHeight cell.Offset(0, 8).Value, msoFalse, msoScaleFromMiddle
            .Left = cell.Offset(0, 9).Value
            .Top = cell.Offset(0, 10).Value
        End With
        
    ElseIf cell.Offset(0, -1).Value = "N" Then 'Unnused slides
        slide.Delete

    End If
    
Next

'Saves presetnation and a copy of the sheet for security
file.SaveCopyAs Sheets("Parameters").Range("C3").Value & Sheets("Filling table").Range("O2").Value & "\Intelligence Report " & Replace(Date, "/", ".") & ".pptx"
file.Close
PPT.Presentations.Open (Sheets("Parameters").Range("C3").Value & Sheets("Filling table").Range("O2").Value & "\Intelligence Report " & Replace(Date, "/", ".") & ".pptx")
ActiveWorkbook.SaveCopyAs (Sheets("Parameters").Range("C4").Value & "Source - Intelligence Report " & Replace(Date, "/", ".") & ".xlsm")

'Writes email
Set olk = New outlook.Application
Set email = olk.CreateItem(olMailItem)

email.Display
email.To = Sheets("Parameters").Range("C5").Value
email.CC = Sheets("Parameters").Range("C6").Value
email.Subject = "Market Intelligence Report " & formt(Date, "dd/mm")
email.Attachments.Add (Sheets("Parameters").Range("C3").Value & Sheets("Filling table").Range("O2").Value & "\Intelligence Report " & Replace(Date, "/", ".") & ".pptx")

'Finishes variables
Set olk = Nothing
Set email = Nothing
Set PPT = Nothing
Set file = Nothing
Set cover = Nothing

End Sub

