Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Load environment variables from .env file
Set objEnvFile = objFSO.OpenTextFile(".env", 1)
Do Until objEnvFile.AtEndOfStream
    strLine = Trim(objEnvFile.ReadLine)
    If strLine <> "" And InStr(strLine, "=") > 0 Then
        arrPair = Split(strLine, "=")
        key = Trim(arrPair(0))
        value = Trim(arrPair(1))
        
        Select Case key
            Case "CLIENT_ID"
                key = "SPOTIPY_CLIENT_ID"
            Case "CLIENT_SECRET"
                key = "SPOTIPY_CLIENT_SECRET"
            Case "REDIRECT_URI"
                key = "SPOTIPY_REDIRECT_URI"
        End Select
        
        objShell.Environment("Process")(key) = value
    End If
Loop
objEnvFile.Close

objShell.Run "python getTopTracks.py", 0, True

Set objFile = objFSO.OpenTextFile("top_tracks.txt", 1)
strLinks = objFile.ReadAll
arrLinks = Split(strLinks, vbCrLf)
objFile.Close

For i = 0 To UBound(arrLinks)
    link = Trim(arrLinks(i))
    If link <> "" Then
        objShell.Run "powershell -NoProfile -ExecutionPolicy Bypass -Command ""spotify_dl -mc 3 -l " & link & " -o 'topTracks'""", 0, True
    End If
Next
