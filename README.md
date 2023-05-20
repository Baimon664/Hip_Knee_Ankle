Load SAM weights from [here](https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth)

# Updated Pipeline:
1. Roboflow (YOLOv8 + pretrained) -> get segmentation result of สะโพก, เข่าบน, เข่าล่าง
2. นำ Segmentation ของสะโพก (Femoral circle) ไปหาสร้างวงกลมแล้วหาจุดกลาง
3. สำหรับเข่าบนเข่าล่าง ไม่ใช้ segment ของ roboflow แต่นำ bounding box ของ roboflow ไปใช้เป็น prompt ให้ SAM ทำ segment แทน
4. นำ Segmentation ของเข่าบนและเข่าล่าง มาหาจุดกลาง
5. ข้อเท้าใช้ template matching กับ algo ในการหา

# Notes:
1. Roboflow segment ออกมาเป็น polygon ซึ่งตำแหน่งของ segmentation ยังหยาบไป
2. Femoral circle หาแค่จุดกลาง จึงพอใช้งานได้
3. SAM ไม่สามารถ segment femoral circle ได้ ถ้าจะลองต้อง finetune SAM [link](https://encord.com/blog/learn-how-to-fine-tune-the-segment-anything-model-sam/) (แต่ส่วนตัวคิดว่าได้ผลไม่น่าต่างกับ roboflow เพราะข้อจำกัดด้านจำนวน dataset)
3. เข่าบนเข่าล่างต้องการผลที่ precise (roboflow ให้ผลมาแบบวงใหญ่ๆ จึงใช้งานได้ยาก)
