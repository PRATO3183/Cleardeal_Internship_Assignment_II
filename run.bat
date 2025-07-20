echo .
echo ========================================
echo RUN bat active
echo ========================================

echo Step 1.....
echo Running uvicorn app.......
call uvicorn backend.app.main:app --reload

