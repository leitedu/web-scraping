Attribute VB_Name = "Relatório"
Sub relatorio()

'Define variables
Dim inicio, obj As Integer
Dim resposta As VbMsgBoxResult
Dim cell As Range

'Define Outlook
Dim olk As outlook.Application
Dim email As outlook.MailItem

'Handles Presentation
Set PPT = CreateObject("PowerPoint.Application")
Set arquivo = PPT.Presentations.Open(Sheets("Parameters").Range("C2").Value) 'Opens presentaion model
Set capa = arquivo.Slides(1)

Sheets("Filling table").Select 'Sheet that controls slides and contents

'Loop for each information added to the report
For Each cell In Range(Range("B3"), Range("B3").End(xlDown))

    Set slide = arquivo.Slides(cell.Offset(0, 2).Value) 'Finds slide where information will be displayed
    slide.Select
    
    If cell.Offset(0, -1).Value = "T" Then 'Text content
        Set forma = slide.Shapes(cell.Offset(0, 7).Value)
        inicio = forma.TextFrame.TextRange.Find(cell.Offset(0, 3).Value).Characters.Start
        forma.TextFrame.TextRange.Characters(inicio).InsertBefore (cell.Offset(0, 4).Value)
        forma.TextFrame.TextRange.Find(cell.Offset(0, 3).Value).Delete

    
    ElseIf cell.Offset(0, -1).Value = "S" Then 'Image content
        Sheets(cell.Offset(0, 5).Value).Range(cell.Offset(0, 3).Value) = cell.Offset(0, 4).Value
        Sheets(cell.Offset(0, 5).Value).Range(cell.Offset(0, 6).Value).CopyPicture Appearance:=xlScreen, Format:=xlPicture
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
arquivo.SaveCopyAs Sheets("Parameters").Range("C3").Value & Sheets("Filling table").Range("O2").Value & "\Intelligence Report " & Replace(Date, "/", ".") & ".pptx"
arquivo.Close
PPT.Presentations.Open (Sheets("Parameters").Range("C3").Value & Sheets("Filling table").Range("O2").Value & "\Intelligence Report " & Replace(Date, "/", ".") & ".pptx")
ActiveWorkbook.SaveCopyAs (Sheets("Parameters").Range("C4").Value & "Base - Intelligence Report " & Replace(Date, "/", ".") & ".xlsm")

'Writes email
Set olk = New outlook.Application
Set email = olk.CreateItem(olMailItem)

email.Display
email.To = Sheets("Parameters").Range("C5").Value
email.CC = Sheets("Parameters").Range("C6").Value
email.Subject = "Market Intelligence Report " & Format(Date, "dd/mm")
email.Attachments.Add (Sheets("Parameters").Range("C3").Value & Sheets("Filling table").Range("O2").Value & "\Intelligence Report " & Replace(Date, "/", ".") & ".pptx")

'Finish variables
Set olk = Nothing
Set email = Nothing
Set PPT = Nothing
Set arquivo = Nothing
Set capa = Nothing

End Sub

