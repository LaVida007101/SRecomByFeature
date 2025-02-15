Dim objFSO, srcFolder, destFolder
Dim objSubFolder, objFile

' Define source and destination folders
srcFolder = "topTracks"  
destFolder = "DailyTracks\daily" 

Set objFSO = CreateObject("Scripting.FileSystemObject")

If objFSO.FolderExists(srcFolder) Then
    If Not objFSO.FolderExists(destFolder) Then
        objFSO.CreateFolder(destFolder)
    End If
    
    For Each objSubFolder In objFSO.GetFolder(srcFolder).SubFolders
        For Each objFile In objSubFolder.Files
            If Not objFSO.FileExists(objFSO.BuildPath(destFolder, objFile.Name)) Then
                objFile.Move objFSO.BuildPath(destFolder, objFile.Name)
            End If
        Next
        objFSO.DeleteFolder objSubFolder, True
    Next
Else
    WScript.Echo "Source folder does not exist."
End If

Set objFSO = Nothing

