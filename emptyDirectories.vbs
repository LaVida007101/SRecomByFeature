Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("Shell.Application")

Dim directories
directories = Array("DailyTracks", "topTracks")

Sub EmptyDirectory(folderPath)
    If objFSO.FolderExists(folderPath) Then
        For Each file In objFSO.GetFolder(folderPath).Files
            file.Delete True
        Next
        For Each subfolder In objFSO.GetFolder(folderPath).SubFolders
            subfolder.Delete True
        Next
    End If
End Sub

For Each dir In directories
    EmptyDirectory dir
Next

objShell.Namespace(10).Items().InvokeVerb("Empty Recycle Bin")

Set objFSO = Nothing
Set objShell = Nothing