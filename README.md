# HexDB
My wife quilts as a hobby and her collection of fabric is awe inspiring. So she asked me to built this database application to help her organize and catalog her fabric.
The application accepts a jpg image and saves information about the image into a SQLite databse as well as saving the image locally for future access.
There is some light automation when the image is uploaded to determine what the dominant color of the fabric is as well as what color family the dominant color belongs to.
The dominant color is determined using a KMeans algorithm to determine the different cluster centers and thus the different colors that makeup the image.
The application then counts the labels for all the pixels to determine which cluster center has the most members.
That RGB value is then fed into a KDTree that allows the dominant cluster center to be matched to one of the exiting CSS3 color names.
That name is then automatically filled into the database.


Future Considerations:
  -Add sorting and search features
  -Implement fabric palette selector mode
  -Implement pattern recognition ai to assist with identification at upload and help determine if there is already identical fabric present in the collection
  -Implement hexy based quilt layout tool
  -(Far Future)Implement a web based or mobile version of the application
